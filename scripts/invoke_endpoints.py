import boto3
import json

# Load endpoint name from SSM
ssm = boto3.client("ssm")
param = ssm.get_parameter(Name="/ml-pipeline/sagemaker/endpoint-name", WithDecryption=False)
endpoint_name = param["Parameter"]["Value"]

# Prompt input
payload = {"inputs": "Today in the world"}

# Invoke endpoint
sm = boto3.client("sagemaker-runtime")
response = sm.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="application/json",
    Body=json.dumps(payload)
)

# Parse result
body = response["Body"].read()
result = json.loads(body)

# Print result
if isinstance(result, list) and "generated_text" in result[0]:
    print("📜 Generated text:", result[0]["generated_text"])
else:
    print("⚠️ Unexpected output format:", result)
