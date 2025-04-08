import os
import boto3
import json

param_name = os.environ.get("ENDPOINT_NAME_PARAM")
if not param_name:
    raise RuntimeError("Missing required environment variable ENDPOINT_NAME_PARAM")


ssm = boto3.client("ssm")
runtime = boto3.client("sagemaker-runtime")

# Load endpoint name from SSM during cold start
ENDPOINT_NAME = ssm.get_parameter(
    Name=os.environ["ENDPOINT_NAME_PARAM"],
    WithDecryption=False
)["Parameter"]["Value"]

def handler(event, context):
    try:
        body = json.loads(event["body"])
        inputs = body.get("inputs")

        if not inputs or not isinstance(inputs, str):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing or invalid 'inputs'"})
            }

        response = runtime.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType="application/json",
            Body=json.dumps({"inputs": inputs})
        )

        result = json.loads(response["Body"].read())

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
