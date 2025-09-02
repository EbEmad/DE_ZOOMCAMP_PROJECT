import psycopg2
import os

def create_table():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="db",
            port="5432"
        )

        cursor = conn.cursor()
        print("✅ Connected to PostgreSQL")

        # Create the table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS world_population (
                country VARCHAR(150),
                population INT,
                ayearly_change NUMERIC(10, 2),
                net_change NUMERIC(10, 2),
                density INT,
                land_area NUMERIC(10, 2),
                migrants INT,
                fert_rate NUMERIC(10, 2),
                med_age NUMERIC(10, 2),
                urban_pop INT,
                world_share NUMERIC(10, 2),
                ins_date VARCHAR(50),
                received_at TIMESTAMP DEFAULT NOW()
            );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("✅ Table created or already exists.")
    except Exception as e:
        print(f"🚨 Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()
 