import os

import pendulum
from airflow.decorators import dag, task

os.environ["UV_CACHE_DIR"] = "/tmp/uv-cache-airflow"


@dag(
    dag_id="05_scheduling_with_venvs",
    schedule=None,
    start_date=pendulum.datetime(year=2025, month=1, day=15),
    catchup=False,
)
def scheduling_with_venvs():
    @task.virtualenv(
        task_id="virtualenv_python",
        requirements=["twelvedata", "pendulum", "lazy_object_proxy", "colorama==0.4.0"],
        system_site_packages=False,
        serializer="cloudpickle",
    )
    def run_with_twelvedata(data_interval_start):
        import pendulum
        import twelvedata
        from colorama import Fore

        print(Fore.GREEN + f"Processing data for interval: {data_interval_start}")
        print(f"Twelvedata version: {twelvedata.__version__}")
        print(f"Pendulum version: {pendulum.__version__}")

        return str(data_interval_start)

    run_with_twelvedata(data_interval_start="{{ data_interval_start }}")


scheduling_with_venvs()
