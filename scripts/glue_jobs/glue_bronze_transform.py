from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import 
from pyspark.sql.functions import col, year, month, to_date
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME", 'TARGET_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Read csv data from the source path using the Glue Catalog.
raw_csv_data = glueContext.create_dynamic_frame.from_catalog(
    database="TODO", table_name="TODO")

# Convert DynamicFrame to DataFrame for transformations
raw_df = raw_csv_data.toDF()

# TODO: Parse year and month from timestamp column
raw_df = raw_df.withColumn("date", to_date(col("timestamp"), "yyyy-MM-dd"))

# Extract year and month
raw_df = raw_df.withColumn("year", year(col("date"))) \
               .withColumn("month", month(col("date")))

# Reduce the number of partitions to minimize the number of parquet files
raw_df = df.coalesce(10)

raw_dynamic_frame = DynamicFrame.fromDF(raw_df, glueContext, "optimized")

# Write data as parquet to the target path
glueContext.write_dynamic_frame.from_options(
    frame=raw_dynamic_frame,
    connection_type="s3",
    connection_options={
        "path": args["TARGET_PATH"],
        "partitionKeys": ["year", "month"]
        },
    format="parquet"
)

job.commit()