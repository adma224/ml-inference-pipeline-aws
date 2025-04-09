import boto3
import json

# Load endpoint name from SSM
ssm = boto3.client("ssm")
param = ssm.get_parameter(Name="/ml-pipeline/sagemaker/endpoint-name", WithDecryption=False)
endpoint_name = param["Parameter"]["Value"]

# SageMaker runtime client
sm = boto3.client("sagemaker-runtime")

print("🧠 GPT-2 Inference Console. Type your prompt below (Ctrl+C to exit).")

try:
    while True:
        prompt = input("\n✏️ Prompt: ").strip()
        if not prompt:
            print("⚠️ Please enter a non-empty prompt.")
            continue

        # Construct payload
        payload = {"inputs": prompt}

        # Invoke endpoint
        response = sm.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="application/json",
            Body=json.dumps(payload)
        )

        # Read and decode result
        body = response["Body"].read()
        result = json.loads(body)


        # Display output
        if isinstance(result, list) and "generated_text" in result[0]:
            print("📜 Generated:", result[0]["generated_text"])
        else:
            print("⚠️ Unexpected output format:", result)

except KeyboardInterrupt:
    print("\n👋 Exiting inference console.")
