import datetime
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from pyspark.sql.functions import col, lit, year, month, to_date, to_timestamp, input_file_name

args = getResolvedOptions(sys.argv, ["JOB_NAME", "TARGET_PATH", "YEAR", "MONTH"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

year = args["YEAR"]
month = args["MONTH"]

predicate = f"year == '{year}' and month == '{month}'"

# Read csv data from the source path using the Glue Catalog.
raw_csv_data = glueContext.create_dynamic_frame.from_catalog(
    database="e-commerce_analytics",
    table_name="raw_ecom_csv",
    push_down_predicate=predicate
)

# Convert DynamicFrame to DataFrame for transformations
raw_df = raw_csv_data.toDF()

# TODO: Parse year and month from timestamp column
raw_df = raw_df.withColumn("event_ts", to_timestamp(col("event_time"), "yyyy-MM-dd HH:mm:ss 'UTC'")) \
               .withColumn("date", to_date(col("event_ts"))) \
               .withColumn("ingestion_ts", lit(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))) \
               .withColumn("input_filename", lit("2019-Oct-enriched.csv"))

# Extract year and month
raw_df = raw_df.withColumn("year", year(col("date"))) \
               .withColumn("month", month(col("date")))


# Reduce the number of partitions to minimize the number of parquet files
raw_df = raw_df.coalesce(10)

raw_dynamic_frame = DynamicFrame.fromDF(raw_df, glueContext, "optimized")

######## Configuration Notes ########
# parameter "enableUpdateCatalog" tells the aws glue job to update #the glue data catalog  as the new partitions are created
# parameter "updateBehavior" set to "UPDATE_IN_DATABASE" to allow updating new partitions
# requires glue table to have parameter useGlueParquetWriter: true
additionalOptions = {"enableUpdateCatalog": True, "updateBehavior": "UPDATE_IN_DATABASE"}
# define the partition keys 
additionalOptions["partitionKeys"] = ["year", "month"]

# Write data as parquet to the target path
sink = glueContext.write_dynamic_frame_from_catalog(
    frame=raw_dynamic_frame, 
    database="e-commerce_analytics",
    table_name="raw_ecom_parquet",
    additional_options=additionalOptions,
    transformation_ctx="bronze_transform_sink"
    )

job.commit()