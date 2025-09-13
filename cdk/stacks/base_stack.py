# stacks/base_stack.py
from aws_cdk import (
    Stack,
    Duration,
    aws_s3 as s3,
    aws_iam as iam,
    aws_ssm as ssm,
)
from constructs import Construct


class BaseStack(Stack):
    """
    Shared primitives:
      - S3 bucket for model artifacts + lifecycle rules
      - SageMaker execution role
      - SSM parameters (bucket name, role ARN)
    """

    @staticmethod
    def bucket_name(domain: str, account: str | None, region: str) -> str:
        left = domain.replace(".", "-").lower()
        acct = (account or "dev").lower()
        return f"{left}-{acct}-{region}-frontend"

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # S3: model artifact + data-capture bucket with lifecycle
        self.artifact_bucket = s3.Bucket(
            self, "ModelArtifactBucket",
            versioned=True,
            auto_delete_objects=False,
            removal_policy=None,
            lifecycle_rules=[
                # Data capture -> Glacier IR after 30d; expire after 365d
                s3.LifecycleRule(
                    id="CaptureToGlacierExpire",
                    prefix="gpt2-v1/data-capture/",
                    transitions=[s3.Transition(
                        storage_class=s3.StorageClass.GLACIER_INSTANT_RETRIEVAL,
                        transition_after=Duration.days(30),
                    )],
                    expiration=Duration.days(365),
                    enabled=True,
                ),
                # Artifacts -> Standard-IA after 30d; prune old versions at 90d
                s3.LifecycleRule(
                    id="ArtifactsToIAWithPruneVersions",
                    prefix="gpt2-v1/",
                    transitions=[s3.Transition(
                        storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                        transition_after=Duration.days(30),
                    )],
                    noncurrent_version_expiration=Duration.days(90),
                    enabled=True,
                ),
            ],
        )

        # SSM: bucket name
        ssm.StringParameter(
            self, "ModelArtifactBucketParam",
            parameter_name="/ml-pipeline/s3/model-artifact-bucket",
            string_value=self.artifact_bucket.bucket_name,
        )

        # IAM: SageMaker execution role
        self.sagemaker_role = iam.Role(
            self, "SageMakerExecutionRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
            ],
        )

        # SSM: role ARN
        ssm.StringParameter(
            self, "SageMakerExecutionRoleParam",
            parameter_name="/ml-pipeline/sagemaker/execution-role-arn",
            string_value=self.sagemaker_role.role_arn,
        )
