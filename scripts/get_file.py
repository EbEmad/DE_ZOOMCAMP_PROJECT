from datetime import date
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()


def get_csv_file(**kwargs):
    try:
        # Retrieve data from XCom
        df = kwargs['ti'].xcom_pull(task_ids='process_data_task')

        # Convert to CSV
        local_file_location = f'./data/world_population_{date.today()}.csv'
        df.to_csv(local_file_location, index=False)
        print(f"CSV file saved to: {local_file_location}")
    except Exception as e:
        raise Exception("Error loading data to csv file:", e) from e