from kafka import KafkaProducer
import json

def send_df_to_kafka(**kwargs):
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
