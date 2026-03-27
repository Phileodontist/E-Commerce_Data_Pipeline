import os
import boto3
from boto3.dynamodb.conditions import Key
    
from infrastructure.schemas.dynamoDB.job_schemas import job_schemas

os.environ.setdefault("AWS_PROFILE", "lpascual")

dynamo_client = boto3.client("dynamodb")

tables = dynamo_client.list_tables()["TableNames"]

if "ecom_jobs" not in tables:
    print("Table creation in progress...")
    response = dynamo_client.create_table(
        AttributeDefinitions=[
            {
                "AttributeName": "PK",
                "AttributeType": "S"
            },
            {
                "AttributeName": "SK",
                "AttributeType": "S"
            }            
        ],
        TableName="ecom_jobs",
        KeySchema=[
            {
                "AttributeName": "PK",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "SK",
                "KeyType": "RANGE"
            }            
        ],
        BillingMode="PAY_PER_REQUEST"
    )
    print(response)
else:
    print("Table already exists. Skipping creation step.")

dynamodb_resource = boto3.resource("dynamodb")
ecom_jobs_table = dynamodb_resource.Table("ecom_jobs")

# Insert job meta records into table (Will overwrite existing records with same PK-SK)
for job_db_schema in job_schemas:
    response = ecom_jobs_table.put_item(Item=job_db_schema)
    print(f"{job_db_schema['PK']}: Status Code ({response['ResponseMetadata']['HTTPStatusCode']})")

# Query the table to verify records were inserted correctly
for job_db_schema in job_schemas:
    response = ecom_jobs_table.query(
        KeyConditionExpression=Key("PK").eq(f"{job_db_schema['PK']}") & Key("SK").eq("META")
    )

    items = response.get("Items", [])
    for item in items:
        print(f"{item['PK']} : {item['description']}")    