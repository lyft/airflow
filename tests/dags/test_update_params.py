import datetime

from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG
from airflow.macros import update_params

DEFAULT_DATE = datetime.datetime(2016, 1, 1)

dag = DAG(
    dag_id='test_update_params',
    start_date=DEFAULT_DATE,
    schedule_interval='@daily',
    max_active_runs=100
)

cmd = """
    {% set params = macros.update_params(params, dag_run) %}
    echo "{{ params.override }}" > {{ dag_run.conf.file_name }}
"""

with dag:
    BashOperator(
        task_id='bash_task',
        bash_command=cmd,
        dag=dag,
        params={"override": "failed"},
    )