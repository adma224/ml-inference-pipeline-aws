import boto3
import os
import mimetypes

# Constants
FRONTEND_DIR = "../webpages/index.html"
SSM_PARAM = "/ml-pipeline/frontend/bucket-name"
ACL_SETTING = "public-read"  # Can be "private" if you're not using public website hosting

# AWS Clients
ssm = boto3.client("ssm")
s3 = boto3.client("s3")
session = boto3.session.Session()
region = session.region_name or "us-east-1"  # Fallback if region isn't set

def get_bucket_name():
    """Fetch the S3 bucket name from SSM Parameter Store"""
    param = ssm.get_parameter(Name=SSM_PARAM, WithDecryption=False)
    return param["Parameter"]["Value"]

def upload_file_to_s3(bucket_name, file_path, key):
    """Upload a single file to S3 with the appropriate content type"""
    content_type, _ = mimetypes.guess_type(file_path)
    try:
        with open(file_path, "rb") as f:
            s3.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=f,
                ContentType=content_type or "binary/octet-stream",
                CacheControl="max-age=86400",  # Cache for 1 day
                ACL=ACL_SETTING
            )
        print(f"✅ Uploaded: {key} ({content_type or 'unknown'})")
        return True
    except Exception as e:
        print(f"❌ Failed to upload {key}: {e}")
        return False

def upload_directory(bucket_name, directory):
    """Recursively upload all files in a directory to S3"""
    success_count = 0
    failure_count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, directory)
            if upload_file_to_s3(bucket_name, full_path, relative_path):
                success_count += 1
            else:
                failure_count += 1
    return success_count, failure_count

if __name__ == "__main__":
    try:
        bucket = get_bucket_name()
        print(f"🌐 Uploading to bucket: {bucket}")
        uploaded, failed = upload_directory(bucket, FRONTEND_DIR)
        print(f"\n📦 Upload summary: {uploaded} files uploaded, {failed} failed.")
        print(f"🚀 Website upload complete!")
        print(f"🔗 Access your site at: http://{bucket}.s3-website-{region}.amazonaws.com")
    except Exception as e:
        print(f"❌ Upload failed: {e}")

