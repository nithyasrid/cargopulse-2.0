import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp, when, lit
from pyspark.sql.types import StructType, StructField, StringType

KAFKA = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
TOPIC = os.getenv("KAFKA_TOPIC", "shipment-events")
POSTGRES = "jdbc:postgresql://postgres:5432/cargopulse"
USER = "cargopulse"
PASSWORD = "cargopulse"

schema = StructType([
    StructField("eventId", StringType(), False),
    StructField("shipmentId", StringType(), False),
    StructField("eventType", StringType(), False),
    StructField("eventTimestamp", StringType(), False),
    StructField("location", StringType(), True),
    StructField("status", StringType(), True),
    StructField("origin", StringType(), True),
    StructField("destination", StringType(), True),
])

spark = (
    SparkSession.builder
    .appName("CargoPulseShipmentStream")
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.4,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA)
    .option("subscribe", TOPIC)
    .option("startingOffsets", "earliest")
    .option("failOnDataLoss", "false")
    .load()
)

events = (
    raw.select(from_json(col("value").cast("string"), schema).alias("e"))
    .select("e.*")
    .withColumn("event_time", to_timestamp("eventTimestamp"))
    .filter(col("eventId").isNotNull() & col("shipmentId").isNotNull())
    .withColumn(
        "is_delayed",
        when(col("status") == "DELAYED", lit(True)).otherwise(lit(False))
    )
)

def write_batch(batch_df, batch_id):
    if batch_df.rdd.isEmpty():
        return

    event_rows = batch_df.select(
        col("eventId").alias("event_id"),
        col("shipmentId").alias("shipment_id"),
        col("eventType").alias("event_type"),
        col("event_time").alias("event_timestamp"),
        "location",
        "status"
    )

    event_rows.write.mode("append").jdbc(
        POSTGRES,
        "shipment_events",
        properties={
            "user": USER,
            "password": PASSWORD,
            "driver": "org.postgresql.Driver",
        },
    )

    latest = (
        batch_df.groupBy("shipmentId")
        .agg(
            {"eventType": "last", "status": "last",
             "location": "last", "event_time": "max"}
        )
    )

    # A deterministic JDBC upsert is intentionally kept in Python for the local MVP.
    rows = latest.collect()
    import psycopg2

    conn = psycopg2.connect(
        host="postgres", dbname="cargopulse", user=USER, password=PASSWORD
    )
    try:
        with conn.cursor() as cur:
            for row in rows:
                shipment_id = row["shipmentId"]
                event_type = row["last(eventType)"]
                status = row["last(status)"]
                location = row["last(location)"]
                event_time = row["max(event_time)"]
                delayed = status == "DELAYED"
                delay = 60.0 if delayed else 0.0
                risk = min(1.0, 0.3 + delay / 180.0) if delayed else 0.05

                cur.execute(
                    """
                    INSERT INTO shipment_analytics
                    (shipment_id,event_count,latest_event_type,latest_status,
                     latest_location,last_event_timestamp,delay_minutes,
                     is_delayed,risk_score,updated_at)
                    VALUES (%s,1,%s,%s,%s,%s,%s,%s,%s,NOW())
                    ON CONFLICT (shipment_id) DO UPDATE SET
                      event_count = shipment_analytics.event_count + 1,
                      latest_event_type = EXCLUDED.latest_event_type,
                      latest_status = EXCLUDED.latest_status,
                      latest_location = EXCLUDED.latest_location,
                      last_event_timestamp = EXCLUDED.last_event_timestamp,
                      delay_minutes = EXCLUDED.delay_minutes,
                      is_delayed = EXCLUDED.is_delayed,
                      risk_score = EXCLUDED.risk_score,
                      updated_at = NOW()
                    """,
                    (shipment_id, event_type, status, location, event_time,
                     delay, delayed, risk),
                )
        conn.commit()
    finally:
        conn.close()

query = (
    events.writeStream
    .foreachBatch(write_batch)
    .option("checkpointLocation", "/tmp/cargopulse-checkpoints/shipment-stream")
    .trigger(processingTime="10 seconds")
    .start()
)

query.awaitTermination()
