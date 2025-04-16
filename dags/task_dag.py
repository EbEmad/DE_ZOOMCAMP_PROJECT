from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta, date
from ..scripts.get_data import fetch_data
from ..scripts.Transform import transform_data
from ..scripts.kafka_producer import send_df_to_kafka
from ..scripts.get_file import get_csv_file
from ..scripts.Create_table import create_table
from ..scripts.terraform import terraform_apply
from ..scripts.Check_table import check_table
from ..scripts.consume_insert import consume_and_insert
from ..scripts.Retrive_Rows import retrieve_rows

# Define the DAG
with DAG(
    'Anas',
    description='A simple DAG for python code',
    start_date=datetime(2025, 4, 15),
    schedule_interval='@weekly',
    catchup=False


) as dag:
     # Define the tasks
    fetch_data_task = PythonOperator(
        task_id='fetch_data_task',
        python_callable=fetch_data
    )

    process_data_task = PythonOperator(
        task_id='process_data_task',
        python_callable=transform_data,
        op_args=[],
        op_kwargs={'doc': "{{ task_instance.xcom_pull(task_ids='fetch_data_task') }}"},
        provide_context=True,
    )

    send_dataframe_to_kafka_task = PythonOperator(
        task_id = 'send_dataframe_to_kafka_task',
        python_callable=send_df_to_kafka
    )

    create_table_task = PythonOperator(
        task_id='create_table_task',
        python_callable=create_table,
        provide_context=True,
    )
    consume_and_insert_task = PythonOperator(
        task_id='consume_and_insert_task',
        python_callable=consume_and_insert,
        op_kwargs={'topic': 'ETL-PROJECT'},
        dag=dag
        
    )
    check_table_task = PythonOperator(
        task_id='check_table_task',
        python_callable=check_table
    )
    retrieve_rows_task = PythonOperator(
        task_id='retrieve_rows_task',
        python_callable=retrieve_rows
    )
    get_csv_file_task = PythonOperator(
        task_id='get_csv_file_task',
        python_callable=get_csv_file
    )
    terraform_apply_task = DockerOperator(
        task_id="terraform_apply_task",
        image="ubuntu:latest",
        api_version="auto",
        auto_remove=False,
        working_dir="/terraform",
        command='/bin/bash -c "terraform init && terraform apply -auto-approve"',
        do_xcom_push=False,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )




    
# Set up task dependencies
    fetch_data_task >> process_data_task
    process_data_task >> send_dataframe_to_kafka_task
    send_dataframe_to_kafka_task >> create_table_task
    create_table_task >> consume_and_insert_task
    consume_and_insert_task >> check_table_task
    check_table_task >> retrieve_rows_task
    process_data_task >> get_csv_file_task
    get_csv_file_task >> terraform_apply_task