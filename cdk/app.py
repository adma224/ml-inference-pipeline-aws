import os
from aws_cdk import App, Environment

from stacks.base_stack import BaseStack
from stacks.ai_stack import AIStack
from stacks.backend_stack import BackendStack
from stacks.frontend_stack import FrontendStack
from stacks.network_stack import NetworkStack

env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-1"),
)

app = App()

base_stack = BaseStack(app, "BaseStack", env=env)

ai_stack = AIStack(app, "AIStack", env=env)

backend_stack = BackendStack(app, "BackendStack", env=env)
backend_stack.add_dependency(ai_stack)

frontend_stack = FrontendStack(
    app, "FrontendStack",
    generate_fn=backend_stack.generate_fn,
    ping_fn=backend_stack.ping_fn,
    vote_fn=backend_stack.vote_fn,
    env=env,
)
frontend_stack.add_dependency(backend_stack)

network_stack = NetworkStack(
    app, "NetworkStack",
    frontend_bucket=frontend_stack.frontend_bucket,
    rest_api=frontend_stack.api,
    domain_name="adrianmurillo.io",
    env=env,
)
network_stack.add_dependency(frontend_stack)

app.synth()