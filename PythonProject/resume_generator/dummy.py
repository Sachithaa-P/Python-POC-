from pyspark.sql.functions import *

# Set up a streaming DataFrame using Auto Loader
df = (spark.readStream
      .format("cloudFiles")
      .option("cloudFiles.format", "json")
      .option("cloudFiles.schemaLocation", "/mnt/schemaLocation")
      .load("/mnt/data/incoming_logs/"))

# Apply schema evolution – allow new columns in incoming data
df = df.selectExpr("timestamp", "user_id", "event_type")

# Write the stream to a Delta table, with schema evolution
df.writeStream \
    .format("delta") \
    .option("mergeSchema", "true")  # Enable schema evolution
    .outputMode("append") \
    .option("checkpointLocation", "/mnt/data/checkpoint/") \
    .start("/mnt/data/delta/log_data")
