from datetime import datetime, timedelta
from io import BytesIO

import polars as pl
import requests
from airflow.decorators import dag, task
from airflow.sdk import ObjectStoragePath

S3_BUCKET = ObjectStoragePath("s3://tariff-distances", conn_id="aws_default")


@dag(
    dag_id="tariff_distances_dataset_pipeline",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2025, 11, 1),
    schedule="@monthly",
    catchup=True,
    max_active_runs=3,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    description="Download and process NYC Yellow Taxi data with monthly backfilling",
)
def nyc_taxi_pipeline():
    @task
    def download_taxi_data(**kwargs) -> str:
        logical_date = kwargs["logical_date"]
        year = logical_date.year
        month = logical_date.month

        print(f"Downloading taxi data for {year}-{month:02d}")

        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"

        try:
            response = requests.get(url, timeout=300)
            response.raise_for_status()

            s3_raw_path = (
                S3_BUCKET / "raw" / f"yellow_tripdata_{year}-{month:02d}.parquet"
            )

            with s3_raw_path.open("wb") as f:
                f.write(response.content)

            file_size_mb = len(response.content) / (1024 * 1024)
            print(f"Downloaded and saved to S3: {s3_raw_path} ({file_size_mb:.2f} MB)")

            return str(s3_raw_path)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading data: {e}")
            raise

    @task
    def process_taxi_data(raw_s3_path: str, **kwargs) -> str:
        logical_date = kwargs["logical_date"]
        year = logical_date.year
        month = logical_date.month

        print(f"Processing taxi data for {year}-{month:02d}")

        s3_path_obj = ObjectStoragePath(raw_s3_path, conn_id="aws_default")

        with s3_path_obj.open("rb") as f:
            parquet_bytes = f.read()

        df = pl.read_parquet(BytesIO(parquet_bytes))

        print(f"Loaded {len(df):,} rows")

        df = df.filter(
            (pl.col("tpep_pickup_datetime").dt.year() == year)
            & (pl.col("tpep_pickup_datetime").dt.month() == month)
        )

        df = df.filter(
            (pl.col("passenger_count") > 0)
            & (pl.col("trip_distance") > 0)
            & (pl.col("fare_amount") > 0)
            & (pl.col("total_amount") > 0)
        )

        print(f"After filtering: {len(df):,} rows")

        daily_df = (
            df.lazy()
            .with_columns(pl.col("tpep_pickup_datetime").dt.date().alias("ride_date"))
            .group_by("ride_date")
            .agg(
                [
                    pl.len().alias("total_rides"),
                    pl.col("passenger_count").sum().alias("total_passengers"),
                    pl.col("trip_distance").mean().alias("avg_trip_distance"),
                    pl.col("trip_distance").sum().alias("total_trip_distance"),
                    pl.col("fare_amount").mean().alias("avg_fare_amount"),
                    pl.col("fare_amount").sum().alias("total_fare_amount"),
                    pl.col("total_amount").mean().alias("avg_total_amount"),
                    pl.col("total_amount").sum().alias("total_amount_sum"),
                    pl.col("tip_amount").mean().alias("avg_tip_amount"),
                    pl.col("tip_amount").sum().alias("total_tip_amount"),
                ]
            )
            .sort("ride_date")
            .collect()
        )

        print(f"Created daily dataset with {len(daily_df)} days")
        print(daily_df.head())

        s3_processed_path = (
            S3_BUCKET / "processed" / f"daily_taxi_data_{year}-{month:02d}.parquet"
        )

        with s3_processed_path.open("wb") as f:
            daily_df.write_parquet(f)

        print(f"Saved processed data to: {s3_processed_path}")

        return str(s3_processed_path)

    raw_path = download_taxi_data()
    processed_path = process_taxi_data(raw_path)
    return processed_path


nyc_taxi_pipeline_dag = nyc_taxi_pipeline()
