from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta, date
import sys
sys.path.append('/opt/airflow/scripts')
from Check_table import check_table
from consume_insert import consume_and_insert
from Create_table import create_table
from get_data import fetch_data
from get_file import get_csv_file
from  kafka_producer import send_df_to_kafka
from  Retrive_Rows import retrieve_rows
from  Transform import transform_data



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
with DAG('test',
         default_args=default_args,
         description='A DAG to fetch and store world population data',
         schedule_interval='@daily',
         catchup=True) as dag:

    # Define the tasks
    fetch_data_task = PythonOperator(
        task_id='fetch_data_task',
        python_callable= fetch_data
    )

    process_data_task = PythonOperator(
        task_id='process_data_task',
        python_callable= transform_data,
        op_args=[],
        op_kwargs={'doc': "{{ task_instance.xcom_pull(task_ids='fetch_data_task') }}"},
        provide_context=True,
    )

    send_dataframe_to_kafka_task = PythonOperator(
        task_id = 'send_dataframe_to_kafka_task',
        python_callable= send_df_to_kafka,
        provide_context=True,
    )

    create_table_task = PythonOperator(
        task_id='create_table_task',
        python_callable=create_table,
        provide_context=True,
    )

    consume_and_insert_task = PythonOperator(
        task_id='consume_and_insert_task',
        python_callable= consume_and_insert
    )

    check_table_task = PythonOperator(
        task_id='check_table_task',
        python_callable= check_table
    )

    retrieve_rows_task = PythonOperator(
        task_id='retrieve_rows_task',
        python_callable= retrieve_rows
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