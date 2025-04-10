import json
import os
import boto3
import time

# Cold start timer
COLD_START = True
cold_start_time = time.time()

def log_json(message, **kwargs):
    print(json.dumps({"message": message, **kwargs}))

def get_env_var(name):
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value

def get_ssm_parameter(name, retries=3, delay=1):
    ssm = boto3.client("ssm")
    for attempt in range(1, retries + 1):
        try:
            return ssm.get_parameter(Name=name)["Parameter"]["Value"]
        except Exception as e:
            log_json("SSMFetchFailed", attempt=attempt, error=str(e))
            time.sleep(delay)
    raise Exception(f"Failed to fetch SSM param: {name}")

def build_response(status, body_dict):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps(body_dict)
    }

def handler(event, context):
    global COLD_START
    if COLD_START:
        log_json("ColdStart", duration_ms=round((time.time() - cold_start_time) * 1000))
        COLD_START = False

    # Handle preflight request
    if event.get("httpMethod") == "OPTIONS":
        return build_response(200, { "message": "CORS preflight OK" })

    try:
        endpoint_param = get_env_var("ENDPOINT_NAME_PARAM")
        endpoint_name = get_ssm_parameter(endpoint_param)
    except Exception as e:
        return build_response(500, { "error": f"SSM fetch failed: {str(e)}" })

    try:
        sm = boto3.client("sagemaker-runtime")
        response = sm.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="application/json",
            Body=json.dumps({ "inputs": "__ping__" })
        )
        result = json.loads(response["Body"].read())
        log_json("PingSuccess", result=result)
        return build_response(200, { "message": "Ping successful", "result": result })

    except Exception as e:
        log_json("PingFailure", error=str(e))
        return build_response(502, { "error": f"Ping failed: {str(e)}" })
