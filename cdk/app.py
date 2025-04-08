#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.infra_stack import InfraStack
from stacks.inference_stack import InferenceStack

app = cdk.App()

infra = InfraStack(app, "InfraStack")

InferenceStack(
    app,
    "InferenceStack",
    artifact_bucket=infra.artifact_bucket,
    sagemaker_role=infra.sagemaker_role
)

app.synth()
