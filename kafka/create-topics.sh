#!/bin/bash

docker exec kafka /opt/bitnami/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --topic ETL-PROJECT \
  --create \
  --partitions 1 \
  --replication-factor 1 \
  --config retention.ms=604800000 \
  --if-not-exists || echo "Topic already exists or creation failed"