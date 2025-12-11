from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_json, to_timestamp, window, avg, max as spark_max
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

def main():
    spark = SparkSession.builder \
        .appName("RealTimeVehicleTracking") \
        .master("local[*]") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # 1️⃣ Schema for incoming JSON data
    gps_schema = StructType([
        StructField("vehicle_id", StringType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True),
        StructField("speed", DoubleType(), True),
        StructField("event_time", StringType(), True)  # will convert to timestamp
    ])

    # 2️⃣ Read stream from Kafka
    raw_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "vehicle_gps") \
        .option("startingOffsets", "latest") \
        .load()

    # Kafka value is bytes → cast to string
    json_df = raw_df.selectExpr("CAST(value AS STRING) AS json_str")

    # 3️⃣ Parse JSON and cast event_time to proper timestamp
    parsed_df = json_df.select(
        from_json(col("json_str"), gps_schema).alias("data")
    ).select(
        col("data.vehicle_id"),
        col("data.latitude"),
        col("data.longitude"),
        col("data.speed"),
        to_timestamp(col("data.event_time")).alias("event_time")
    )

    # 4️⃣ Simple overspeed alert (speed > 80 km/h)
    alerts_df = parsed_df.where(col("speed") > 80)

    # 5️⃣ Average speed per vehicle in last 5 minutes (sliding every 1 minute)
    windowed_stats_df = parsed_df \
        .withWatermark("event_time", "10 minutes") \
        .groupBy(
            window(col("event_time"), "5 minutes", "1 minute"),
            col("vehicle_id")
        ) \
        .agg(
            avg("speed").alias("avg_speed"),
            spark_max("speed").alias("max_speed")
        )

    # 6️⃣ Write raw stream to console (for debugging)
    raw_query = parsed_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .queryName("raw_gps_stream") \
        .start()

    # 7️⃣ Write alerts to console
    alerts_query = alerts_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .queryName("overspeed_alerts") \
        .start()

    # 8️⃣ Write aggregated stats to console
    stats_query = windowed_stats_df.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", "false") \
        .queryName("vehicle_speed_stats") \
        .start()

    # 9️⃣ Keep the streaming queries running
    spark.streams.awaitAnyTermination()

if __name__ == "__main__":
    main()
