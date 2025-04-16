from kafka import KafkaProducer
import json

def send_df_to_kafka(**kwargs):
    producer=None
    try:
        # initialize the Kafka producer
        producer=KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: json.dumps(x, default=str).encode('utf-8')
        )
        df = kwargs['ti'].xcom_pull(task_ids='Transform_data')

        # convert DataFrame to dictionary records
        df=df.to_dict(orient='records')

        # send each record to Kafka topic
        for record in df:
            producer.send('ETL-PROJECT', value=record)
            print(f"Sent record: {record}")
        

        # ensure all messages are sent 
        producer.flush()
        print("All records sent successfully.")
    except Exception as e:
        print(f"Error sending records to Kafka: {e}")
        raise
    finally:
        if producer:
            producer.close()
            print("Kafka producer closed.")
