from kafka import KafkaConsumer
import os
import json
import psycopg2
from dotenv import load_dotenv
load_dotenv()
def consume_and_insert():
    consumer = None
    conn = None
    cursor = None
    
    try:
        # Initialize Kafka consumer
        consumer = KafkaConsumer(
            os.getenv("KAFKA_TOPIC", "ETL-PROJECT"),
            bootstrap_servers=['kafka:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='etl-consumer-group',
            client_id=f'etl-consumer-client-{str(uuid.uuid4())}',
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000,
            max_poll_interval_ms=300000
        )
        
        print("📡 Kafka consumer started. Waiting for partition assignment...")
        
        # Wait for partition assignment
        consumer.poll(timeout_ms=10000)
        if not consumer.assignment():
            print("⚠️ No partitions assigned after 10 seconds")
            return

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

        # Process messages
        for message in consumer:
            try:
                if not message.value:
                    print("⚠️ Empty message received")
                    continue
                    
                record = message.value
                
                # Validate required fields
                required_fields = ['country', 'population', 'ayearly_change', 'net_change',
                                 'density', 'land_area', 'migrants', 'fert_rate',
                                 'med_age', 'urban_pop', 'world_share', 'ins_date']
                
                if not all(field in record for field in required_fields):
                    print(f"⚠️ Missing fields in message: {record}")
                    continue
                
                # Insert into PostgreSQL
                insert_query = """
                    INSERT INTO world_population (
                        country, population, ayearly_change, net_change, density,
                        land_area, migrants, fert_rate, med_age, urban_pop,
                        world_share, ins_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                
                cursor.execute(insert_query, (
                    record['country'],
                    record['population'],
                    record['ayearly_change'],
                    record['net_change'],
                    record['density'],
                    record['land_area'],
                    record['migrants'],
                    record['fert_rate'],
                    record['med_age'],
                    record['urban_pop'],
                    record['world_share'],
                    record['ins_date']
                ))
                conn.commit()
                
                # Manually commit offset
                consumer.commit()
                
                print(f"📥 Inserted record: {record['country']}")
                
            except KeyError as e:
                print(f"🚨 Missing expected field in message: {e}")
                if conn:
                    conn.rollback()
            except Exception as e:
                print(f"🚨 Error processing message: {e}")
                if conn:
                    conn.rollback()
                
    except Exception as e:
        print(f"🚨 Critical error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        if consumer:
            consumer.close()
        print("🔌 Resources cleaned up")