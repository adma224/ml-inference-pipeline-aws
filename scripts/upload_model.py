import os
import tarfile
import boto3
import datetime

REGION = os.getenv("AWS_REGION", "us-east-1")

# Initialize clients
ssm = boto3.client("ssm", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)

# Get S3 bucket name from SSM
param = ssm.get_parameter(Name="/ml-pipeline/s3/model-artifact-bucket", WithDecryption=False)
BUCKET_NAME = param["Parameter"]["Value"]

# Define model packaging info
MODEL_DIR = "models/gpt2-v1/gpt2_finetuned"
VERSION_TAG = datetime.datetime.now().strftime("v%Y%m%d-%H%M%S")
OUTPUT_PATH = f"/tmp/model-{VERSION_TAG}.tar.gz"
DEST_KEY = f"gpt2-v1/{VERSION_TAG}/model.tar.gz"

# Create tar.gz archive
with tarfile.open(OUTPUT_PATH, "w:gz") as tar:
    tar.add(MODEL_DIR, arcname=".") 

print(f"✅ Model tarball created: {OUTPUT_PATH}")

# Upload model artifacts to S3
s3.upload_file(OUTPUT_PATH, BUCKET_NAME, DEST_KEY)
print(f"🚀 Uploaded to s3://{BUCKET_NAME}/{DEST_KEY}")

# Store latest model version in SSM
ssm.put_parameter(
    Name="/ml-pipeline/model/latest-version",
    Value=VERSION_TAG,
    Type="String",
    Overwrite=True
)
print(f"📌 Updated SSM with latest model version: {VERSION_TAG}")



