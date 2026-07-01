import boto3
from botocore.exceptions import ClientError

from config.infra_config import *
from infrastructure.schemas.glue.datalake_schemas import * 

# -----------------------------
# Spark -> Glue type conversion
# -----------------------------
def spark_to_glue_type(spark_type):
    mapping = {
        "IntegerType": "int",
        "LongType": "bigint",
        "StringType": "string",
        "BooleanType": "boolean",
        "TimestampType": "timestamp",
        "FloatType": "float",
        "DoubleType": "double"
    }
    return mapping.get(spark_type, "string")

# -----------------------------
# Convert StructType -> Glue Columns
# -----------------------------
def convert_schema(struct_type):
    cols = []
    for field in struct_type.fields:
        glue_type = spark_to_glue_type(type(field.dataType).__name__)
        cols.append({
            "Name": field.name,
            "Type": glue_type
        })
    return cols

# -----------------------------
# Create Glue Table
# -----------------------------
def create_glue_table(
    glue_client,
    database,
    table_name,
    schema,
    s3_location,
    partitions=None
):
    try:
        glue_client.get_table(DatabaseName=database, Name=table_name)
        print(f"Table '{table_name}' already exists in database '{database}'.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityNotFoundException':
            print(f"Table '{table_name}' does not exist. Creating...")
            columns = convert_schema(schema)

            partition_keys = []
            if partitions:
                for p in partitions:
                    partition_keys.append({"Name": p, "Type": "string"})

            response = glue_client.create_table(
                DatabaseName=database,
                TableInput={
                    "Name": table_name,
                    "TableType": "EXTERNAL_TABLE",
                    "StorageDescriptor": {
                        "Columns": columns,
                        "Location": s3_location,
                        "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
                        "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
                        "SerdeInfo": {
                            "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe",
                            "Parameters": {"serialization.format": "1"}
                        }
                    },
                    "PartitionKeys": partition_keys,
                    "Parameters": {
                        "classification": "parquet",
                        "EXTERNAL": "TRUE"
                    }
                }
            )

            print(f"Created table: {table_name}")
            return response

# -----------------------------
# Glue Client
# -----------------------------
glue = boto3.client("glue", region_name="us-west-1")

# -----------------------------
# Create Silver Tables
# -----------------------------
product_schema = silver_schemas["product"]
event_schema = silver_schemas["event"]
user_schema = silver_schemas["user"]

schemas = [product_schema, event_schema, user_schema]
table_names = ["silver_" + name for name in silver_schemas.keys()]

for table_name, schema in zip(table_names, schemas):
    partitions = None
    s3_path = S3_NORMALIZED_PATH
    if "event" in table_name:
        partitions = ["year", "month"]

    create_glue_table(
        glue,
        DB_NAME,
        table_name,
        schema,
        s3_path,
        partitions=partitions
    )

# -----------------------------
# Create Gold Tables
# -----------------------------
fact_view_schema = gold_schemas["fact_view"]
fact_engagement_schema = gold_schemas["fact_engagement"]
dim_product_schema = gold_schemas["dim_product"]
dim_user_schema = gold_schemas["dim_user"]
dim_date_schema = gold_schemas["dim_date"]

schemas = [fact_view_schema, fact_engagement_schema, dim_product_schema, dim_user_schema, dim_date_schema]
table_names = gold_schemas.keys()

for table_name, schema in zip(table_names, schemas):
    partitions = None
    if "fact" in table_name:
        partitions = ["year", "month"]
        s3_path = S3_FACTS_PATH
    else:
        s3_path = S3_DIMENSIONS_PATH

    create_glue_table(
        glue,
        DB_NAME,
        table_name,
        schema,
        s3_path,
        partitions=partitions
    )