from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime,timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Define the DAG
with DAG(
    'HemaDag',
    description='A simple DAG for python code',
    start_date=datetime(2025, 4, 6),
    schedule_interval='@weekly',
    catchup=False


) as dag:
    fetch_data= BashOperator(
        task_id='fetch_data',
        bash_command='python3 /opt/airflow/scripts/Extract.py',
        dag=dag
    )
    transform_data= BashOperator(
        task_id='Transform_data',
        bash_command='python3 /opt/airflow/scripts/Transform.py',
        dag=dag
    )

    fetch_data >> transform_data
    