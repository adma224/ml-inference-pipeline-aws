#!/usr/bin/env python3

import os
from aws_cdk import App, Environment

from stacks.base_stack import BaseStack
from stacks.ai_stack import AIStack
from stacks.backend_stack import BackendStack
from stacks.frontend_stack import FrontendStack

# 🌍 Set target environment from AWS credentials
env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-1")
)

app = App()

# 1️⃣ Base resources: S3 bucket + IAM + SSM
base_stack = BaseStack(app, "BaseStack", env=env)

# 2️⃣ ML deployment: SageMaker model + endpoint
ai_stack = AIStack(app, "AIStack", env=env)

# 3️⃣ Backend API logic: Lambda functions
backend_stack = BackendStack(app, "BackendStack", env=env)

# 4️⃣ Frontend & API Gateway
frontend_stack = FrontendStack(
    app, "FrontendStack",
    generate_fn=backend_stack.generate_fn,
    ping_fn=backend_stack.ping_fn,
    vote_fn=backend_stack.vote_fn,  # ✅ Now using vote_fn
    env=env
)

app.synth()
