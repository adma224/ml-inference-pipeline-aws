#!/usr/bin/env python3
import os
from aws_cdk import App, Environment

# Your stacks
from stacks.base_stack import BaseStack
from stacks.ai_stack import AIStack
from stacks.backend_stack import BackendStack
from stacks.frontend_stack import FrontendStack
from stacks.edge_stack import EdgeStack
from stacks.network_stack import NetworkStack  # should only do API custom domain + DNS

# ----- Config -----
DOMAIN = "adrianmurillo.io"

ACCOUNT = os.getenv("CDK_DEFAULT_ACCOUNT")
PRIMARY_REGION = os.getenv("CDK_DEFAULT_REGION", "us-east-1")  # your main region
EDGE_REGION = "us-east-1"  # CloudFront/ACM must be here

env_primary = Environment(account=ACCOUNT, region=PRIMARY_REGION)
env_edge = Environment(account=ACCOUNT, region=EDGE_REGION)

# Optional: deterministic bucket name (unique per account+region)
def bucket_name(domain: str, account: str | None, region: str) -> str:
    # bucket names must be lowercase and globally unique
    left = domain.replace(".", "-").lower()
    acct = (account or "dev").lower()
    return f"{left}-{acct}-{region}-frontend"

app = App()

# ----- Core / Data plane -----
base_stack = BaseStack(app, "BaseStack", env=env_primary)

ai_stack = AIStack(app, "AIStack", env=env_primary)

backend_stack = BackendStack(app, "BackendStack", env=env_primary)
backend_stack.add_dependency(ai_stack)

# ----- Frontend (S3 + API Gateway) -----
frontend_stack = FrontendStack(
    app, "FrontendStack",
    generate_fn=backend_stack.generate_fn,
    ping_fn=backend_stack.ping_fn,
    vote_fn=backend_stack.vote_fn,
    # You can set None to let CDK name the bucket,
    # or use the helper below for a stable, unique name:
    bucket_name=bucket_name(DOMAIN, ACCOUNT, PRIMARY_REGION),
    env=env_primary,
)
frontend_stack.add_dependency(backend_stack)

# ----- Edge (CloudFront + us-east-1 cert + DNS for apex/www) -----
edge_stack = EdgeStack(
    app, "EdgeStack",
    website_bucket=frontend_stack.frontend_bucket,
    env=env_edge,
)
edge_stack.add_dependency(frontend_stack)  # ensure bucket exists before CF

# ----- Network (API custom domain: api.<domain>) -----
network_stack = NetworkStack(
    app, "NetworkStack",
    rest_api=frontend_stack.api,
    domain_name=DOMAIN,
    env=env_primary,
)
network_stack.add_dependency(frontend_stack)

app.synth()
