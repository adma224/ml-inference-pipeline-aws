# stacks/base_stack.py
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_ssm as ssm,
)
from constructs import Construct


class BaseStack(Stack):
    """
    Shared primitives used by other stacks:
    - Versioned S3 bucket for model artifacts.
    - SageMaker execution role with S3 read and SageMaker full access.
    - SSM parameters exposing bucket name and role ARN.

    Also hosts deterministic naming helpers (e.g., website bucket).
    """

    @staticmethod
    def bucket_name(domain: str, account: str | None, region: str) -> str:
        """
        Deterministic website bucket name (must be globally unique and lowercase).
        Example: adrianmurillo-io-123456789012-us-east-1-frontend
        """
        left = domain.replace(".", "-").lower()
        acct = (account or "dev").lower()
        return f"{left}-{acct}-{region}-frontend"

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # S3: model artifact bucket (versioned). Keep objects by default.
        self.artifact_bucket = s3.Bucket(
            self,
            "ModelArtifactBucket",
            versioned=True,
            auto_delete_objects=False,  # safer for learning and audit
            removal_policy=None,        # preserve on stack delete
        )

        # SSM: publish bucket name for consumers (AIStack)
        ssm.StringParameter(
            self,
            "ModelArtifactBucketParam",
            parameter_name="/ml-pipeline/s3/model-artifact-bucket",
            string_value=self.artifact_bucket.bucket_name,
        )

        # IAM: minimal SageMaker execution role for model hosting
        self.sagemaker_role = iam.Role(
            self,
            "SageMakerExecutionRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
            ],
        )

        # SSM: publish role ARN for consumers (AIStack)
        ssm.StringParameter(
            self,
            "SageMakerExecutionRoleParam",
            parameter_name="/ml-pipeline/sagemaker/execution-role-arn",
            string_value=self.sagemaker_role.role_arn,
        )

