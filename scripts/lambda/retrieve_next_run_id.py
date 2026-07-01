import json
import boto3
import logging
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_next_run_id(job_name: str, table_name: str) -> int:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    pk_value = f"{job_name}"

    response = table.query(
        KeyConditionExpression=Key("PK").eq(pk_value) &
                               Key("SK").begins_with("RUN#"),
        ScanIndexForward=False,   # DESC -> latest run first
        Limit=1                   # only need the newest run
    )

    items = response.get("Items", [])
    return int(items[0]["SK"].split("#")[1]) if items else 0

def lambda_handler(event, context):
    """
    Lambda function to retrieve the next run ID for a given job and table.
    """
    logger.info(f"Received event: {json.dumps(event)}")

    current_run_id = get_next_run_id(event["job_name"], event["table_name"])

    result = {"status": "success", "next_run_id": str(current_run_id + 1)}

    logger.info(f"Results: {json.dumps(result)}")

    return {
        "statusCode": 200,
        "body": result
    }