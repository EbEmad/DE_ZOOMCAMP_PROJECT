
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
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

def fetch_data(**kwargs):
    try:
        url = "https://www.worldometers.info/world-population/population-by-country/"
        requested_result = requests.get(url).text
        doc = BeautifulSoup(requested_result, 'html.parser')
        print("Connection to the website established.")
        return doc
    except Exception as e:
        raise Exception("CONNECTION ERROR: Can't connect to the website to fetch the data!") from e

def process_data(doc, **kwargs):
    try:
        order = []
        country = []
        population = []
        yearly_change = []
        net_change = []
        density = []
        land_area = []
        migrants = []
        fert_rate = []
        med_age = []
        urban_pop = []
        world_share = []
        ins_date = []
        whole_data = {}

        # to fetch the variable from prev function
        doc = fetch_data()

        container = doc.find_all("div", class_="not-prose")
        table_child = container[0].find_all("table")
        table_row = table_child[0].find_all("tr")

        headers = table_row[0].find_all("th")
        headers_list = [header.get_text() for header in headers]

        for row in table_row[1:]:
            row_elements = row.find_all("td")

            #order
            try:
                order.append(int(row_elements[0].get_text()))
            except:
                order.append(-1)

            # country
            try:
                country.append(str(row_elements[1].get_text()))
            except:
                country.append('N/A')

            # population
            try:
                population.append(int(row_elements[2].get_text().replace(',', '')))
            except:
                population.append(0)

            # yearly_change
            try:
                yearly_change.append(float(row_elements[3].string.strip().split(' ')[0]))
            except:
                yearly_change.append(0)

            # net_change
            try:
                net_change.append(float(row_elements[4].string.strip().replace(',', '')))
            except:
                net_change.append(0)

            # density
            try:
                density.append(int(row_elements[5].string.strip().replace(',', '')))
            except:
                density.append(0)

            # land_area
            try:
                land_area.append(float(row_elements[6].string.strip().replace(',', '')))
            except:
                land_area.append(0)

            # migrants
            try:
                migrants.append(int(row_elements[7].string.strip().replace(',', '')))
            except:
                migrants.append(0)

            # fert_rate
            try:
                fert_rate.append(float(row_elements[8].string.strip()))
            except:
                med_age.append(0)

            # med_age
            try:
                med_age.append(int(row_elements[9].string.strip()))
            except:
                med_age.append(0)

            # urban_pop
            try:
                urban_pop.append(int(row_elements[10].string.strip().split(' ')[0]))
            except:
                urban_pop.append(0)

            # world_share
            try:
                world_share.append(float(row_elements[11].string.strip().split(' ')[0]))
            except:
                world_share.append(0)

            # inserted_date
            ins_date.append(str(datetime.now()))

        ziped_lists = list(zip(order, country, population, yearly_change, net_change, density, land_area, migrants, fert_rate, med_age, urban_pop, world_share, ins_date))
    
        try:
            whole_data.clear()
            order.clear()
            country.clear()
            population.clear()
            yearly_change.clear()
            net_change.clear()
            density.clear()
            land_area.clear()
            migrants.clear()
            fert_rate.clear()
            med_age.clear()
            urban_pop.clear()
            world_share.clear()
            ins_date.clear()
        except:
            raise Exception("Can't clear the lists!")
        else:
            print("Lists are clear!")
    
        try:
            for o, c, p, y, n, d, l, m, f, g, u, w, t in ziped_lists:
                order.append(o)
                country.append(c)
                population.append(p)
                yearly_change.append(y)
                net_change.append(n)
                density.append(d)
                land_area.append(l)
                migrants.append(m)
                fert_rate.append(f)
                med_age.append(g)
                urban_pop.append(u)
                world_share.append(w)
                ins_date.append(t)
        except:
            raise Exception("Can't add data into lists!")
        else:
            print('Lists are full of data!')

        whole_data = {
            f"{headers_list[1].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : country,
            f"{headers_list[2].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : population,
            f"{headers_list[3].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : yearly_change,
            f"{headers_list[4].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : net_change,
            f"{headers_list[5].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : density,
            f"{headers_list[6].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : land_area,
            f"{headers_list[7].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : migrants,
            f"{headers_list[8].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : fert_rate,
            f"{headers_list[9].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : med_age,
            f"{headers_list[10].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : urban_pop,
            f"{headers_list[11].split('(')[0].split('%')[0].replace('.', '').strip().replace(' ', '_').upper()}" : world_share,
            'INS_DATE': ins_date
        }

        # create pandas dataframe for data
        df = pd.DataFrame(data=whole_data)

        print("Data processing complete.")
        return df
    except Exception as e:
        raise Exception("Error processing data:", e) from e
    
def send_dataframe_to_kafka(**kwargs):
    producer = None
    try:
        # Initialize Kafka producer
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda x: json.dumps(x, default=str).encode('utf-8')
        )

        df = kwargs['ti'].xcom_pull(task_ids='process_data_task')

        # Convert DataFrame to dictionary records
        records = df.to_dict(orient='records')
        
        # Send each record to Kafka
        for record in records:
            producer.send('ETL-PROJECT', value=record)
        
        # Ensure all messages are sent
        producer.flush()
        print(f"Successfully sent {len(records)} records to Kafka topic: ETL-PROJECT")
        
    except Exception as e:
        print(f"Error sending data to Kafka: {str(e)}")
        raise
    finally:
        if producer:
            producer.close()

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

def retrieve_rows():
    try:
        conn_string = f'postgresql+psycopg2://root:root@db:5432/test'
        engine = create_engine(conn_string)
        with engine.connect() as conn:
            # Create a SQLAlchemy text object for your query
            query = text("SELECT * FROM world_population LIMIT 10")
            result = conn.execute(query)
            for row in result:
                print(row)
    except Exception as e:
        raise Exception("Error retrieving rows:", e) from e
    
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

# Define the DAG
with DAG('world_population_ETL_dag_43',
         default_args=default_args,
         description='A DAG to fetch and store world population data',
         schedule_interval='@daily',
         catchup=True) as dag:

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
        python_callable=send_dataframe_to_kafka,
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