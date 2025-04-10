#!/usr/bin/env python3

import os
from aws_cdk import App, Environment

from stacks.base_stack import BaseStack
from stacks.ai_stack import AIStack
from stacks.backend_stack import BackendStack
from stacks.frontend_stack import FrontendStack

# Set environment from current AWS credentials
env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-1")
)

app = App()

# 1. Create foundational resources: S3 + IAM role
base_stack = BaseStack(app, "BaseStack", env=env)

# 2. Create SageMaker Model + Endpoint, reads values from SSM (created by BaseStack)
ai_stack = AIStack(app, "AIStack", env=env)

# 3. Deploy Lambda Functions (generate, ping, flag)
backend_stack = BackendStack(app, "BackendStack", env=env)

# 4. Expose API Gateway + static frontend website
frontend_stack = FrontendStack(
    app, "FrontendStack",
    generate_fn=backend_stack.generate_fn,
    ping_fn=backend_stack.ping_fn,
    flag_fn=backend_stack.flag_fn,
    env=env
)

app.synth()

