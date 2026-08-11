#!/usr/bin/env bash
set -e
docker compose up -d postgres kafka spark spark-worker
echo "Waiting for Kafka/Postgres..."
sleep 12
docker compose exec spark spark-submit \
  --master spark://spark:7077 \
  --packages org.postgresql:postgresql:42.7.4,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2 \
  /opt/spark-apps/shipment_stream.py
