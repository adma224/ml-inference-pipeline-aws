#!/usr/bin/env python3

import os
from aws_cdk import App, Environment

from stacks.infra_stack import InfraStack
from stacks.inference_stack import InferenceStack
from stacks.api_stack import ApiStack

# CDK environment (use env vars or hardcode)
env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-1")
)

app = App()

# Deploy InfraStack: S3 + IAM role
infra_stack = InfraStack(app, "InfraStack", env=env)

# Extract bucket name and role ARN to pass to the next stack
bucket_name = infra_stack.artifact_bucket.bucket_name
role_arn = infra_stack.sagemaker_role.role_arn

# Deploy InferenceStack: SageMaker model + endpoint
inference_stack = InferenceStack(
    app, "InferenceStack",
    artifact_bucket_name=bucket_name,
    sagemaker_role_arn=role_arn,
    env=env
)



# Deploy ApiStack: Lambda + API Gateway (uses fixed endpoint name)
api_stack = ApiStack(
    app, "ApiStack",
    endpoint_name="gpt2-endpoint",  # Must match what's defined in inference_stack.py
    env=env
)

app.synth()

