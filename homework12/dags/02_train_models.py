from datetime import datetime, timedelta
from io import BytesIO

import joblib
import polars as pl
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import ObjectStoragePath
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR

S3_BUCKET = ObjectStoragePath("s3://tariff-distances", conn_id="aws_default")


@dag(
    dag_id="taxi_model_training_pipeline",
    start_date=datetime(2025, 12, 1),
    schedule="@monthly",
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    description="Train ML models to predict total_amount for taxi rides",
)
def train_models_pipeline():
    @task
    def fetch_and_prepare_data(**kwargs):
        print("Fetching all processed data from S3...")

        processed_path = S3_BUCKET / "processed"
        all_files = list(processed_path.iterdir())

        print(f"Found {len(all_files)} processed files")

        dfs = []
        for file_path in sorted(all_files):
            if file_path.name.endswith(".parquet"):
                print(f"Loading {file_path.name}")
                with file_path.open("rb") as f:
                    df = pl.read_parquet(BytesIO(f.read()))
                    dfs.append(df)

        full_df = pl.concat(dfs).sort("ride_date")
        print(f"Total dataset size: {len(full_df)} rows")
        print(full_df.head())

        full_df = full_df.with_columns(
            pl.col("ride_date").dt.year().alias("year"),
            pl.col("ride_date").dt.month().alias("month"),
        )

        unique_months = (
            full_df.select(["year", "month"]).unique().sort(["year", "month"])
        )
        print(f"Available months: {len(unique_months)}")

        last_year = unique_months[-1, "year"]
        last_month = unique_months[-1, "month"]

        train_df = full_df.filter(
            ~((pl.col("year") == last_year) & (pl.col("month") == last_month))
        )
        test_df = full_df.filter(
            (pl.col("year") == last_year) & (pl.col("month") == last_month)
        )

        print(f"Training set: {len(train_df)} rows")
        print(f"Test set: {len(test_df)} rows")

        feature_cols = [
            "total_rides",
            "total_passengers",
            "avg_trip_distance",
            "total_trip_distance",
            "avg_fare_amount",
            "total_fare_amount",
            "avg_tip_amount",
            "total_tip_amount",
        ]
        target_col = "avg_total_amount"

        X_train = train_df.select(feature_cols).to_numpy()
        y_train = train_df.select(target_col).to_numpy().flatten()

        X_test = test_df.select(feature_cols).to_numpy()
        y_test = test_df.select(target_col).to_numpy().flatten()

        train_data_path = S3_BUCKET / "ml" / "train_data.joblib"
        test_data_path = S3_BUCKET / "ml" / "test_data.joblib"

        with train_data_path.open("wb") as f:
            joblib.dump({"X": X_train, "y": y_train}, f)

        with test_data_path.open("wb") as f:
            joblib.dump({"X": X_test, "y": y_test}, f)

        print("Data prepared and saved to S3")

        return {
            "train_path": str(train_data_path),
            "test_path": str(test_data_path),
            "train_size": len(train_df),
            "test_size": len(test_df),
        }

    @task
    def train_ridge_model(data_info: dict) -> dict:
        print("Training Ridge Regression model...")

        train_path = ObjectStoragePath(data_info["train_path"], conn_id="aws_default")
        test_path = ObjectStoragePath(data_info["test_path"], conn_id="aws_default")

        with train_path.open("rb") as f:
            train_data = joblib.load(f)
        with test_path.open("rb") as f:
            test_data = joblib.load(f)

        X_train, y_train = train_data["X"], train_data["y"]
        X_test, y_test = test_data["X"], test_data["y"]

        param_grid = {"alpha": [0.1, 1.0, 10.0, 100.0]}

        ridge = Ridge()
        grid_search = GridSearchCV(
            ridge, param_grid, cv=5, scoring="neg_mean_absolute_error", n_jobs=-1
        )
        grid_search.fit(X_train, y_train)

        print(f"Best parameters: {grid_search.best_params_}")

        best_model = grid_search.best_estimator_

        y_pred = best_model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)

        print(f"Ridge Regression MAE: {mae:.4f}")

        model_path = S3_BUCKET / "ml" / "models" / "ridge_model.joblib"
        with model_path.open("wb") as f:
            joblib.dump(best_model, f)

        return {
            "model_name": "Ridge Regression",
            "model_path": str(model_path),
            "mae": mae,
            "train_size": data_info["train_size"],
        }

    @task
    def train_random_forest_model(data_info: dict) -> dict:
        print("Training Random Forest model...")

        train_path = ObjectStoragePath(data_info["train_path"], conn_id="aws_default")
        test_path = ObjectStoragePath(data_info["test_path"], conn_id="aws_default")

        with train_path.open("rb") as f:
            train_data = joblib.load(f)
        with test_path.open("rb") as f:
            test_data = joblib.load(f)

        X_train, y_train = train_data["X"], train_data["y"]
        X_test, y_test = test_data["X"], test_data["y"]

        model = RandomForestRegressor(
            n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)

        print(f"Random Forest MAE: {mae:.4f}")

        model_path = S3_BUCKET / "ml" / "models" / "random_forest_model.joblib"
        with model_path.open("wb") as f:
            joblib.dump(model, f)

        return {
            "model_name": "Random Forest",
            "model_path": str(model_path),
            "mae": mae,
            "train_size": data_info["train_size"],
        }

    @task
    def train_svm_model(data_info: dict) -> dict:
        print("Training SVM model...")

        train_path = ObjectStoragePath(data_info["train_path"], conn_id="aws_default")
        test_path = ObjectStoragePath(data_info["test_path"], conn_id="aws_default")

        with train_path.open("rb") as f:
            train_data = joblib.load(f)
        with test_path.open("rb") as f:
            test_data = joblib.load(f)

        X_train, y_train = train_data["X"], train_data["y"]
        X_test, y_test = test_data["X"], test_data["y"]

        subset_size = min(5000, len(X_train))  # spedup training
        model = SVR(kernel="rbf", C=10.0, epsilon=0.1)
        model.fit(X_train[:subset_size], y_train[:subset_size])

        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)

        print(f"SVM MAE: {mae:.4f}")

        model_path = S3_BUCKET / "ml" / "models" / "svm_model.joblib"
        with model_path.open("wb") as f:
            joblib.dump(model, f)

        return {
            "model_name": "SVM",
            "model_path": str(model_path),
            "mae": mae,
            "train_size": data_info["train_size"],
        }

    @task
    def select_best_model(model_results: list) -> dict:
        print("Selecting best model...")
        print(f"Model results: {model_results}")

        best_model = min(model_results, key=lambda x: x["mae"])
        print(
            f"Best model: {best_model['model_name']} with MAE: {best_model['mae']:.4f}"
        )

        best_model_src = ObjectStoragePath(
            best_model["model_path"], conn_id="aws_default"
        )
        best_model_dest = S3_BUCKET / "ml" / "best_model.joblib"

        with best_model_src.open("rb") as src, best_model_dest.open("wb") as dest:
            dest.write(src.read())

        print(f"Best model saved to: {best_model_dest}")

        for model_result in model_results:
            if model_result["model_name"]:
                clean_path = model_result["model_path"].replace(
                    "s3://aws_default@", "s3://"
                )
                model_path = ObjectStoragePath(clean_path, conn_id="aws_default")

                print(f"Deleting {model_result['model_name']} from {model_path}")
                try:
                    if model_path.exists():
                        model_path.unlink()
                        print(f"Successfully deleted {model_path}")
                    else:
                        print(f"File does not exist: {model_path}")
                except Exception as e:
                    print(f"Could not delete {model_path}: {e}")

        return best_model

    @task
    def log_to_postgres(model_results: list, **kwargs):
        print("Logging model performances to Postgres...")

        postgres_hook = PostgresHook(postgres_conn_id="model_result_storage")
        training_date = kwargs["logical_date"].date()

        for model_result in model_results:
            insert_query = """
                INSERT INTO model_performance (training_date, model_name, training_set_size, mae)
                VALUES (%s, %s, %s, %s)
            """

            postgres_hook.run(
                insert_query,
                parameters=(
                    training_date,
                    model_result["model_name"],
                    model_result["train_size"],
                    model_result["mae"],
                ),
            )

            print(f"Logged {model_result['model_name']}: MAE={model_result['mae']:.4f}")

        print("All model performances logged to database")

    data_info = fetch_and_prepare_data()

    ridge_result = train_ridge_model(data_info)
    rf_result = train_random_forest_model(data_info)
    svm_result = train_svm_model(data_info)

    all_results = [ridge_result, rf_result, svm_result]

    _ = select_best_model(all_results)

    log_to_postgres(all_results)


train_models_dag = train_models_pipeline()
