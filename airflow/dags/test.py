from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta, date
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
import json
from kafka import KafkaProducer, KafkaConsumer
import psycopg2
import pyarrow as pa
import os
import docker
from dotenv import load_dotenv
import uuid
import os
import json
import uuid
import psycopg2
from kafka import KafkaConsumer
load_dotenv()


# Define the default arguments for the DAG
default_args = {
    'owner': 'givi-abe',
    'depends_on_past': False,
    'start_date': datetime(2025, 7, 31),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay':timedelta(minutes=2)
}




# Define the DAG
with DAG('world_population_ETL_dag_43',
         default_args=default_args,
         description='A DAG to fetch and store world population data',
         schedule_interval='@daily',
         catchup=True) as dag:

    # Define the tasks
    fetch_data_task = BashOperator(
        task_id='fetch_data_task',
        bash_command='cd /opt/airflow/scripts && python get_data.py'
    )

    process_data_task = BashOperator(
        task_id='process_data_task',
        bash_command='cd /opt/airflow/scripts && python Transform.py',
        op_args=[],
        op_kwargs={'doc': "{{ task_instance.xcom_pull(task_ids='fetch_data_task') }}"},
        provide_context=True,
    )

    send_dataframe_to_kafka_task = BashOperator(
        task_id = 'send_dataframe_to_kafka_task',
        bash_command='cd /opt/airflow/scripts && python kafka_producer.py',
        provide_context=True,
    )

    create_table_task = BashOperator(
        task_id='create_table_task',
        bash_command='cd /opt/airflow/scripts && python Create_table.py',
        provide_context=True,
    )

    consume_and_insert_task = BashOperator(
        task_id='consume_and_insert_task',
        bash_command='cd /opt/airflow/scripts && python consume_insert.py'
    )

    check_table_task = BashOperator(
        task_id='check_table_task',
        bash_command='cd /opt/airflow/scripts && python Check_table.py'
    )

    retrieve_rows_task = BashOperator(
        task_id='retrieve_rows_task',
        bash_command='cd /opt/airflow/scripts && python Retrive_Rows.py'
    )
    get_csv_file_task = BashOperator(
        task_id='get_csv_file_task',
        bash_command='cd /opt/airflow/scripts && python get_file.py'
    )

  

 

    # Set up task dependencies
    fetch_data_task >> process_data_task
    process_data_task >> send_dataframe_to_kafka_task
    send_dataframe_to_kafka_task >> create_table_task
    create_table_task >> consume_and_insert_task
    consume_and_insert_task >> check_table_task
    check_table_task >> retrieve_rows_task
    process_data_task >> get_csv_file_task