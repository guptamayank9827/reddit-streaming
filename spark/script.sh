#!/bin/bash

# Submit preprocess_job.py to Spark cluster
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
  --driver-memory 512m \
  --executor-memory 512m \
  --conf spark.streaming.backpressure.enabled=true \
  --conf spark.streaming.kafka.maxRatePerPartition=500 \
  --conf spark.executor.instances=1 \
  entity_recognition_streaming.py kafka:9092 topic1 topic2