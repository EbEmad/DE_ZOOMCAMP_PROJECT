from kafka import KafkaConsumer
import os
import json
import psycopg2
from dotenv import load_dotenv
load_dotenv()
def consume_and_insert():
    consumer = KafkaConsumer(
        os.getenv("KAFKA_TOPIC"),
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='my-group',
        consumer_timeout_ms=1000
    )
    
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

        for message in consumer:
            record = message.value
            print(f"Received record: {record}")  # Debugging line to inspect the received record

            # Ensure that the message contains the expected fields
            index = record.get('index')
            country = record.get('country')
            population = record.get('population')
            yearly_change = record.get('yearly_change')
            net_change = record.get('net_change')
            density = record.get('density')
            land_area = record.get('land_area')
            migrants = record.get('migrants')
            fert_rate = record.get('fert_rate')
            median_age = record.get('median_age')
            urban_pop = record.get('urban_pop')
            world_share = record.get('world_share')

            # Insert into PostgreSQL
            insert_query = """
                INSERT INTO world_population (
                    index, country, population, yearly_change, net_change, density, land_area,
                    migrants, fert_rate, median_age, urban_pop, world_share
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                index, country, population, yearly_change, net_change, density, land_area,
                migrants, fert_rate, median_age, urban_pop, world_share
            ))

            # Commit after each insert
            conn.commit()
            print(f"✅ Inserted record into PostgreSQL: {record}")

    except Exception as e:
        print(f"❌ Error consuming messages: {e}")
    
    finally:
        cursor.close()
        conn.close()
        print("✅ PostgreSQL connection closed")