import os

import pendulum
from airflow.decorators import dag, task
from airflow.models import Variable

os.environ["UV_CACHE_DIR"] = "/tmp/uv-cache-airflow"


@dag(
    dag_id="07_connections_and_variables",
    schedule=None,
    start_date=pendulum.datetime(year=2025, month=1, day=15),
    catchup=False,
)
def connections_and_variables():
    @task.virtualenv(
        task_id="virtualenv_python",
        requirements=["twelvedata", "pendulum", "apache-airflow-providers-postgres"],
        system_site_packages=False,
    )
    def run_with_postgres_storage(api_key, symbol, data_interval_start_str):
        import pendulum
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        from twelvedata import TDClient

        def fetch_data(dt_start_str, api_key, symbol):
            td = TDClient(apikey=api_key)
            dt = pendulum.parse(dt_start_str)

            ts = td.exchange_rate(
                symbol=symbol,
                date=dt.isoformat(),
            )
            data = ts.as_json()

            if not data:
                raise ValueError(f"No data returned for symbol: {symbol}")
            return data

        def save_data(data):
            pg_hook = PostgresHook(postgres_conn_id="aiflow_second_storage")

            sql = """
                INSERT INTO exchange_rates (symbol, rate)
                VALUES (%(symbol)s, %(rate)s)
                ON CONFLICT (symbol) 
                DO UPDATE SET rate = EXCLUDED.rate;
            """

            parameters = {"symbol": data["symbol"], "rate": float(data["rate"])}
            pg_hook.run(sql, parameters=parameters)

        print(f"Starting fetch for {symbol}...")
        data = fetch_data(data_interval_start_str, api_key, symbol)

        print(f"Fetched data: {data}. Saving to database...")
        save_data(data)
        print("Done!")

    twelve_api_key = Variable.get("TWELVEDATA_API_KEY")

    run_with_postgres_storage(
        api_key=twelve_api_key,
        symbol="BTC/USD",
        data_interval_start_str="{{ data_interval_start }}",
    )


connections_and_variables()
