#!/usr/bin/env python3

import os
from aws_cdk import App, Environment

from stacks.base_stack import BaseStack
from stacks.ai_stack import AIStack
from stacks.backend_stack import BackendStack
from stacks.frontend_stack import FrontendStack
from stacks.network_stack import NetworkStack


"""
    app.py

    Entry point for the AWS CDK application. This script defines the deployment
    sequence of all infrastructure stacks in the ML inference pipeline project.

    Stacks:
    - BaseStack: foundational IAM, S3, and SSM resources
    - AIStack: SageMaker model and endpoint resources
    - BackendStack: Aurora Serverless SQL database, Lambda functions, and SSM integration
    - FrontendStack: S3-hosted static frontend with API Gateway + Lambda integration

    Stack dependencies:
    - BackendStack depends on AIStack (for SageMaker endpoint in SSM)
    - FrontendStack depends on BackendStack (for Lambda references)
"""


"""
    Environment setup
    Uses AWS CLI profile values for account and region
"""

env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-1")
)


"""
    CDK application definition
"""

app = App()


"""
    Stack deployment order
"""

# Shared resources (IAM, S3, SSM parameters)
base_stack = BaseStack(app, "BaseStack", env=env)

# SageMaker model + endpoint
ai_stack = AIStack(app, "AIStack", env=env)

# Lambda functions, Aurora DB, DBInit Lambda
backend_stack = BackendStack(app, "BackendStack", env=env)
backend_stack.add_dependency(ai_stack)

# Static frontend + API Gateway integration
frontend_stack = FrontendStack(
    app, "FrontendStack",
    generate_fn=backend_stack.generate_fn,
    ping_fn=backend_stack.ping_fn,
    vote_fn=backend_stack.vote_fn,
    env=env
)
frontend_stack.add_dependency(backend_stack)


"""
    Synthesize CloudFormation templates
"""

# Network stack (CloudFront, ACM, Route 53)
network_stack = NetworkStack(
    app, "NetworkStack",
    frontend_bucket=frontend_stack.frontend_bucket,
    domain_name="adrianmurillo.io",
    env=env
)
network_stack.add_dependency(frontend_stack)  # ✅ explicit dependency


app.synth()
