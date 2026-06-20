import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
from pyspark.sql import functions as F
# Read Raw Data
df = spark.read.format("parquet").load("s3://ish-nyc-taxi-data/raw/yellow_taxi/2025/")
df.printSchema()
df = df.toDF(*[c.lower() for c in df.columns])
# raw count 
df.cache()
raw_count = df.count()
# Handle Nulls
df = df.fillna({"passenger_count": 0,
                 "ratecodeid": 0,
                 "airport_fee": 0,
                 "congestion_surcharge": 0,
                 "store_and_fwd_flag": "Unknown"})
# Data Quality Flag
df = df.withColumn("data_quality_flag",
    F.when(
        (F.col("trip_distance") > 0) &
        (F.col("fare_amount") > 0) &
        (F.col("tpep_dropoff_datetime") > F.col("tpep_pickup_datetime")),
        "VALID"
    ).otherwise("INVALID")
)
# Filter Valid records
df_clean = df.filter(F.col("data_quality_flag") == "VALID")
# Date & time columns
df_clean = df_clean.withColumn("pickup_date",F.to_date("tpep_pickup_datetime"))\
       .withColumn("pickup_year",F.year("tpep_pickup_datetime"))\
       .withColumn("pickup_month",F.month("tpep_pickup_datetime"))
df_clean = df_clean.withColumn("trip_duration_minutes",F.round((F.unix_timestamp("tpep_dropoff_datetime")- F.unix_timestamp("tpep_pickup_datetime"))/60,2))
# Filter only year 2025
print("Records before year filter:", df_clean.count())
df_clean = df_clean.filter(F.col("pickup_year")== 2025)
print("Records after year filter:", df_clean.count())
# compare before and after counts
df_clean.cache()
final_count = df_clean.count()
print("Raw:", raw_count)
print("Final:", final_count)
print("Removed:", raw_count - final_count)
#Schema validation
df_clean.printSchema()
# Write Silver Layer
df_clean.write.format("parquet").mode("overwrite").option("overwriteSchema", "true")\
  .partitionBy("pickup_year", "pickup_month")\
  .save("s3://ish-nyc-taxi-data/silver/yellow_taxi/")
job.commit()