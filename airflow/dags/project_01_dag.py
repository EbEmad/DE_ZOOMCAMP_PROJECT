from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta, date
from scripts.Fetch_Data import fetch_data
from scripts.Process_Data import process_data
from scripts.Kafka_Producer import send_df_to_kafka
from scripts.Create_Table import create_table
from scripts.Consume_Insert import consume_and_insert
from scripts.Check_Table import check_table
from scripts.Retrive_Rows import retrieve_rows
from scripts.Get_File import get_csv_file

# Define the default arguments for the DAG
default_args = {
    'owner': 'Ebrahim-Emad',
    'start_date': datetime(2025, 7, 31),
    'retries': 1,
    'retry_delay':timedelta(minutes=2)
}

# Define the DAG
with DAG('world_population_ETL_dag_43',
         default_args=default_args,
         description='A DAG to fetch and store world population data',
         schedule_interval='@daily',
         catchup=False) as dag:

    # Define the tasks
    fetch_data_task = PythonOperator(
        task_id='fetch_data_task',
        python_callable=fetch_data
    )

    process_data_task = PythonOperator(
        task_id='process_data_task',
        python_callable=process_data,
        op_args=[],
        op_kwargs={'doc': "{{ task_instance.xcom_pull(task_ids='fetch_data_task') }}"},
        provide_context=True,
    )

    send_dataframe_to_kafka_task = PythonOperator(
        task_id = 'send_dataframe_to_kafka_task',
        python_callable=send_df_to_kafka,
        provide_context=True,
    )

    create_table_task = PythonOperator(
        task_id='create_table_task',
        python_callable=create_table,
        provide_context=True,
    )

    consume_and_insert_task = PythonOperator(
        task_id='consume_and_insert_task',
        python_callable=consume_and_insert
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

  

 

    # Set up task dependencies
    fetch_data_task >> process_data_task
    process_data_task >> send_dataframe_to_kafka_task
    send_dataframe_to_kafka_task >> create_table_task
    create_table_task >> consume_and_insert_task
    consume_and_insert_task >> check_table_task
    check_table_task >> retrieve_rows_task
    process_data_task >> get_csv_file_task