import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()

def check_table():
    try:
        conn_string = f'postgresql+psycopg2://root:root@db:5432/test'
      
        engine = create_engine(conn_string)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='world_population' AND column_name='con_id')")).scalar()

            if not result:
                conn.execute(text('ALTER TABLE world_population ADD COLUMN con_id SERIAL PRIMARY KEY;'))
                print("Primary key column added to table.")
            else:
                print("Primary key column already exists in table.")

    except Exception as e:
        print(f"Error checking table: {e}") # Print the error
        raise  