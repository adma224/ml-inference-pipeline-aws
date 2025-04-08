import requests
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def get_api_url():
    try:
        ssm = boto3.client("ssm")
        param = ssm.get_parameter(Name="/ml-pipeline/api/url", WithDecryption=False)
        return param["Parameter"]["Value"]
    except ClientError as e:
        print(f"❌ SSM ClientError: {e.response['Error']['Message']}")
    except BotoCoreError as e:
        print(f"❌ BotoCoreError while accessing SSM: {e}")
    except Exception as e:
        print(f"❌ Unexpected error retrieving API URL from SSM: {e}")
    return None

def main():
    api_url = get_api_url()
    if not api_url:
        print("⚠️ Unable to retrieve API URL. Exiting.")
        return

    print("🧠 Enter a prompt (CTRL+C to quit):")

    try:
        while True:
            prompt = input("\n> ").strip()
            if not prompt:
                print("⚠️ Prompt is empty. Please enter a valid sentence.")
                continue

            payload = {"inputs": prompt}

            try:
                response = requests.post(
                    api_url,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(payload),
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and "generated_text" in result[0]:
                        print("📜 Generated:", result[0]["generated_text"])
                    else:
                        print("⚠️ Unexpected response format:", result)
                else:
                    print(f"❌ HTTP {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"❌ Request failed: {e}")

    except KeyboardInterrupt:
        print("\n👋 Exiting gracefully...")

if __name__ == "__main__":
    main()

