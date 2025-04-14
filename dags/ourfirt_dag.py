from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'erbarhim emad',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)

}
with DAG (
    dag_id='our_first_dag',
    default_args=default_args,
    description='My first dag created by erbarhim emad',
    start_date=datetime(2023, 10, 1),
    schedule_interval='@daily',


)as dag:
    task1=BashOperator(
        task_id='first_task',
        bash_command="echo Hello world this is the first task ",

    )
    task2=BashOperator(
        task_id='second_task',
        bash_command="echo Hello world this is the second task ",
    )

    task1>>task2