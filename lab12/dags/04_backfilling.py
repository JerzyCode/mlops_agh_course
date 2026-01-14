from datetime import datetime, timedelta

import pandas as pd
import requests
from airflow.decorators import dag, task


@dag(
    dag_id="weather_backfilling_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=timedelta(days=7),
    catchup=True,
)
def weather_backfilling_pipeline():
    @task
    def fetch_and_save_weather(**kwargs):
        start_dt = kwargs["logical_date"]
        end_dt = start_dt + timedelta(days=6)

        start_str = start_dt.strftime("%Y-%m-%d")
        end_str = end_dt.strftime("%Y-%m-%d")

        print(f"Fetching forecast for period: {start_str} to {end_str}")

        url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude=40.7143&longitude=-74.006&"
            f"start_date={start_str}&end_date={end_str}&"
            f"daily=temperature_2m_max,temperature_2m_min&"
            f"timezone=auto"
        )

        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()

        df = pd.DataFrame(
            {
                "date": data["daily"]["time"],
                "temp_max": data["daily"]["temperature_2m_max"],
                "temp_min": data["daily"]["temperature_2m_min"],
            }
        )

        filename = f"weather_forecast_{start_str}.csv"
        df.to_csv(filename, index=False)
        print(f"Saved to {filename}")

    fetch_and_save_weather()


weather_backfilling_pipeline()
