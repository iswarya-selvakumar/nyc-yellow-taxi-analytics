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

df =spark.read.format("parquet").load("s3://ish-nyc-taxi-data/silver/yellow_taxi/")
df.cache()
df.printSchema()
# Zone reference
zone_df = spark.read.format("csv").options(header=True,inferSchema=True)\
            .load("s3://ish-nyc-taxi-data/reference/taxi_zone_lookup.csv")
zone_df.printSchema()
# columns name 
zone_df = zone_df.toDF(*[c.lower() for c in zone_df.columns])
fact_trip = df.select("vendorid",
                      "tpep_pickup_datetime",
                      "tpep_dropoff_datetime",
                      "pickup_date","pickup_year",
                      "pickup_month",
                      "ratecodeid",
                      "pulocationid",
                      "dolocationid",
                      "payment_type",
                      "passenger_count",
                      "trip_distance",
                      "trip_duration_minutes",
                      "fare_amount",
                      "extra",
                      "mta_tax",
                      "tip_amount",
                      "tolls_amount",
                      "improvement_surcharge",
                      "congestion_surcharge",
                      "airport_fee",
                      "cbd_congestion_fee",
                      "total_amount")

fact_trip.write.format("parquet").mode("overwrite")\
               .partitionBy("pickup_year","pickup_month").save("s3://ish-nyc-taxi-data/gold/fact_trip/")
# Create Dimensional
dim_payment = df.select("payment_type").distinct()
dim_payment = dim_payment.withColumn("payment_type_desc",
         F.when(F.col("payment_type") == 0, "Flex Fare Trip")
          .when(F.col("payment_type") == 1, "Credit Card")
          .when(F.col("payment_type") == 2, "Cash")
          .when(F.col("payment_type") == 3, "No Charge")
          .when(F.col("payment_type") == 4, "Dispute")
          .when(F.col("payment_type") == 5, "Unknown")
          .when(F.col("payment_type") == 6, "Voided Trip")
          .otherwise("Invalid")
)
dim_payment.write.format("parquet").mode("overwrite").save("s3://ish-nyc-taxi-data/gold/dim_payment/")
# Create vendor Dimensional 
dim_vendor = df.select("vendorid").distinct()
dim_vendor = dim_vendor.withColumn("vendor_name",
        F.when(F.col("vendorid") == 1, "Creative Mobile Technologies, LLC")
         .when(F.col("vendorid") == 2, "Curb Mobility, LLC")
         .when(F.col("vendorid") == 6, "Myle Technologies Inc")
         .when(F.col("vendorid") == 7, "Helix")
         .otherwise("Unknown"))
dim_vendor.write.format("parquet").mode("overwrite").save("s3://ish-nyc-taxi-data/gold/dim_vendor/")
# Create date Dimensional
dim_date = df.select("pickup_date").distinct()
dim_date = dim_date.withColumn("year",F.year("pickup_date"))\
                   .withColumn("month",F.month("pickup_date"))\
                   .withColumn("day", F.dayofmonth("pickup_date")) \
                   .withColumn("day_of_week", F.dayofweek("pickup_date")) \
                   .withColumn("week_of_year", F.weekofyear("pickup_date"))
dim_date.write.format("parquet").mode("overwrite").save("s3://ish-nyc-taxi-data/gold/dim_date")
# Create 
dim_ratecode = df.select("ratecodeid").distinct()
dim_ratecode = dim_ratecode.withColumn("ratecodeid_desc",
    F.when(F.col("ratecodeid") == 1, "Standard rate")
     .when(F.col("ratecodeid") == 2, "JFK")
     .when(F.col("ratecodeid") == 3, "Newark")
     .when(F.col("ratecodeid") == 4, "Nassau or Westchester")
     .when(F.col("ratecodeid") == 5, "Negotiated fare")
     .when(F.col("ratecodeid") == 6, "Group ride")
     .when(F.col("ratecodeid") == 99, "Unknown")
     .otherwise("Invalid")
)
dim_ratecode.write.format("parquet").mode("overwrite").save("s3://ish-nyc-taxi-data/gold/dim_ratecode/")
# location 
pickup_location = df.select(F.col("pulocationid").alias("locationid"))
dropoff_location = df.select(F.col("dolocationid").alias("locationid"))
# combine 2 dfs
dim_location = pickup_location.union(dropoff_location).distinct()
dim_location =dim_location.join(zone_df,"locationid","left")
dim_location.write.format("parquet").mode("overwrite").save("s3://ish-nyc-taxi-data/gold/dim_location/")

job.commit()