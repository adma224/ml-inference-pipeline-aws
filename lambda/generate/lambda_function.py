import os
import json
import time
import boto3
import logging
from botocore.exceptions import ClientError

# ----------------------
# Structured Logging Setup (console-only)
# ----------------------
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Used to measure cold start time
COLD_START = True
cold_start_time = time.time()

def log_json(message, **kwargs):
    print(json.dumps({"message": message, **kwargs}))

def get_env_var(name):
    value = os.getenv(name)
    if value is None:
        log_json("MissingEnvVar", var=name)
        raise RuntimeError(f"Environment variable '{name}' is not set.")
    return value

def get_ssm_parameter(name, retries=3, delay=1):
    ssm = boto3.client("ssm")
    for attempt in range(1, retries + 1):
        try:
            value = ssm.get_parameter(Name=name)["Parameter"]["Value"]
            log_json("SSMFetchSuccess", name=name, attempt=attempt)
            return value
        except ClientError as e:
            log_json("SSMFetchFailure", error=str(e), name=name, attempt=attempt)
            time.sleep(delay)
    raise Exception(f"Failed to fetch parameter '{name}' after {retries} retries")

def build_response(status_code, body_dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps(body_dict)
    }

# ----------------------
# Lambda Handler
# ----------------------
def handler(event, context):
    global COLD_START

    if COLD_START:
        log_json("ColdStart", duration_ms=round((time.time() - cold_start_time) * 1000))
        COLD_START = False

    # Preflight request handling
    if event.get("httpMethod") == "OPTIONS":
        return build_response(200, {"message": "CORS preflight OK"})

    # Parse and validate input
    try:
        body = json.loads(event.get("body", "{}"))
        prompt = body.get("inputs")
        if not prompt:
            return build_response(400, {"error": "Missing or empty 'inputs' field."})
    except json.JSONDecodeError:
        return build_response(400, {"error": "Invalid JSON payload."})

    # Retrieve SageMaker endpoint name from SSM
    try:
        endpoint_param = get_env_var("ENDPOINT_NAME_PARAM")
        endpoint_name = get_ssm_parameter(endpoint_param)
    except Exception as e:
        return build_response(500, {"error": f"Failed to fetch endpoint name: {str(e)}"})

    # Invoke SageMaker
    try:
        sm = boto3.client("sagemaker-runtime")
        response = sm.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="application/json",
            Body=json.dumps({"inputs": prompt})
        )
        result = json.loads(response["Body"].read())
        log_json("InferenceSuccess", prompt=prompt, result=result)
        return build_response(200, result)

    except Exception as e:
        log_json("SageMakerInvocationFailure", error=str(e))
        return build_response(502, {"error": f"SageMaker invocation failed: {str(e)}"})
