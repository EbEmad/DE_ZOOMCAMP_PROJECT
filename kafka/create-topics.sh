#!/bin/bash

echo "Waiting for Kafka broker to be available..."

# Wait until the broker responds to metadata requests
until /opt/bitnami/kafka/bin/kafka-topics.sh \
  --bootstrap-server kafka:9092 \
  --list &>/dev/null; do
  echo "Kafka not ready yet..."
  sleep 2
done

echo "Kafka is ready. Creating topic..."

# Now create the topic
/opt/bitnami/kafka/bin/kafka-topics.sh \
  --bootstrap-server kafka:9092 \
  --topic ETL-PROJECT \
  --create \
  --partitions 1 \
  --replication-factor 1 \
  --config retention.ms=604800000 \
  --if-not-exists \
  || echo "Topic already exists or creation failed"
