#!/usr/bin/env python3

import os
from aws_cdk import App, Environment

from stacks.base_stack import BaseStack
from stacks.ai_stack import AIStack
from stacks.backend_stack import BackendStack
from stacks.frontend_stack import FrontendStack

env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-1"),
)

app = App()

# 1. Core infra: S3 bucket + IAM role
base_stack = BaseStack(app, "BaseStack", env=env)

# 2. SageMaker model + endpoint
ai_stack = AIStack(app, "AIStack", env=env)

# 3. Lambda backend
backend_stack = BackendStack(app, "BackendStack", env=env)
backend_stack.add_dependency(ai_stack)

# 4. Frontend + API Gateway
frontend_stack = FrontendStack(
    app, "FrontendStack",
    generate_fn=backend_stack.generate_fn,
    ping_fn=backend_stack.ping_fn,
    flag_fn=backend_stack.flag_fn,
    env=env,
)
frontend_stack.add_dependency(backend_stack)

app.synth()

