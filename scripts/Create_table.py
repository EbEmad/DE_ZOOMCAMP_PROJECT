import psycopg2
import os

def create_table():
    try:
        # connect to postgres
        conn=psycopg2.connect(

            database="airflow",
            user="airflow",
            password="airflow",
            host="postgres",
            port="5432"
        )
        cursor = conn.cursor()

        print("✅ Connected to PostgreSQL")


        # create table
        create_table_query = """ 
            create table if not exists world_population(
            index int,
            country varchar(150),
            population int,
            YearlyChange numeric(10,2),
            netchange numeric(10,2),
            density int,
            land_area numeric(10,2),
            migrants int,
            fert_rate numeric(10,2),
            median_age numeric(10,2),
            urban_pop numeric(10,2),
            world_share numeric(10,2)   
            );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("✅ Table created successfully")
    except Exception as e:
        print(f"❌ Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()
        print("✅ PostgreSQL connection closed") 