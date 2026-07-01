import os
import json
import boto3
import logging
from datetime import datetime
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def retrieve_date_metadata(file_name:str) -> dict:
    metadata = {}
    components = file_name.split("/")
    for com in components:
        if "%3D" in com:
            k, v = com.split("%3D")
            metadata[k] = v
    return metadata

def start_step_function_execution(state_machine_arn: str, input_data: dict, name:str) -> str:
    try:
        # Validate ARN
        if not isinstance(state_machine_arn, str) or not state_machine_arn.startswith("arn:aws:states:"):
            raise ValueError("Invalid state machine ARN.")

        sfn_client = boto3.client("stepfunctions")

        # Prepare parameters
        params = {"stateMachineArn": state_machine_arn}
        if input_data is not None:
            if not isinstance(input_data, dict):
                raise ValueError("input_data must be a dictionary.")
            params["input"] = json.dumps(input_data)
        if name:
            params["name"] = name  # Must be unique per execution

        # Start execution
        response = sfn_client.start_execution(**params)
        print(f"Execution started successfully: {response['executionArn']}")
        return response["executionArn"]

    except (BotoCoreError, ClientError) as e:
        print(f"AWS error: {e}")
    except ValueError as ve:
        print(f"Validation error: {ve}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")

def lambda_handler(event, context):
    """
    Lambda function to retrieve the next run ID for a given job and table.
    """
    logger.info(f"Received event: {json.dumps(event)}")

    event = event["Records"][0]

    partition_metadata = retrieve_date_metadata(event["s3"]["object"]["key"])

    payload = {
        "partition_metadata": partition_metadata,
        "file_metadata": {
            "bucket": event["s3"]["bucket"]["name"],
            "schema_version": event["s3"]["s3SchemaVersion"],
            "input_file": event["s3"]["object"]["key"],
            "input_file_size": event["s3"]["object"]["size"]
        }
    }

    logger.info(f"payload: {json.dumps(payload)}")

    execution_name = "ecom-sfn-"+ ((datetime.now()).strftime('%Y-%m-%d-%H%M%S'))

    start_step_function_execution(
        state_machine_arn=os.environ['stateMachineArn'],
        input_data=payload,
        name=execution_name
    )

    return {
        "statusCode": 200,
        "message": "Step Function execution started successfully"
    }