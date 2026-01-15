# Labolatory Part

## First run


Not working :(

![Not working](imgs/not_working.png)


## Pipe 01 

Pipe 1 - not working again :(

![alt text](imgs/not_working_pipe01.png)
)

Found mistake: no pyarrow lib was included in pyproject.toml


## Exercise 1

Pipeline in file `02_class_pipeline.py`.

![Exercise 1](imgs/exercise1.png)


## Exercise 2

Code in file `04_backfilling.py`


The task were run. However, final task received bad request response code.

![Exercise 2](imgs/exercise_2.png)


## Docker Airflow Deployment

![alt text](imgs/docker-success.png)

## Exercise 3

Code for that exercise is in the `dags/05_scheduling_with_venvs.py` file.


After multiple tries, I was managed to run it fully with all libraries. 

![alt text](imgs/exercise4.png)

The main problem was with permissions with uv `$CACHE_DIR`. To solve it I found 2 solutions:

1. os.environ["UV_CACHE_DIR"] = "/tmp/uv-cache-airflow"
2. os.environ["UV_NO_CACHE"] = "1"



```bash
[2026-01-15 17:37:29] INFO - error: failed to open file `/opt/airflow/.uv-cache/CACHEDIR.TAG`: Permission denied (os error 13) source=airflow.providers.standard.utils.python_virtualenv loc=python_virtualenv.py:161
[2026-01-15 17:37:29] ERROR - Task failed with exception source=task loc=task_runner.py:1008
CalledProcessError: Command '['uv', 'venv', '--allow-existing', '--seed', '--python', 'python', '/tmp/venvdz5r6gig']' returned non-zero exit status 2.
File "/home/airflow/.local/lib/python3.11/site-packages/airflow/sdk/execution_time/task_runner.py", line 934 in run

File "/home/airflow/.local/lib/python3.11/site-packages/airflow/sdk/execution_time/task_runner.py", line 1325 in _execute_task

File "/home/airflow/.local/lib/python3.11/site-packages/airflow/sdk/bases/operator.py", line 417 in wrapper

File "/home/airflow/.local/lib/python3.11/site-packages/airflow/sdk/bases/decorator.py", line 252 in execute

File "/home/airflow/.local/lib/python3.11/site-packages/airflow/sdk/bases/operator.py", line 417 in wrapper

File "/home/airflow/.local/lib/python3.11/site-packages/airflow/providers/standard/operators/python.py", line 490 in execute

File "/home/airflow/.local/lib/python3.11/site-packages/airflow/sdk/bases/operator.py", line 417 in wrapper

File "/home/airflow/.local/lib/python3.11/site-packages/airflow/providers/standard/operators/python.py", line 215 in execute

File "/home/airflow/.local/lib/python3.11/site-packages/airflow/providers/standard/operators/python.py", line 896 in execute_callable

File "/home/airflow/.local/lib/python3.11/site-packages/airflow/providers/standard/operators/python.py", line 774 in _prepare_venv

File "/home/airflow/.local/lib/python3.11/site-packages/airflow/providers/standard/utils/python_virtualenv.py", line 205 in prepare_virtualenv

File "/home/airflow/.local/lib/python3.11/site-packages/airflow/providers/standard/utils/python_virtualenv.py", line 165 in _execute_in_subprocess

```