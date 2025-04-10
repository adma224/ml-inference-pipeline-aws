from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_ssm as ssm,
)
from constructs import Construct


class BaseStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 📦 S3 Bucket for model artifacts
        self.artifact_bucket = s3.Bucket(
            self, "ModelArtifactBucket",
            versioned=True,
            auto_delete_objects=False,  # safer in production
            removal_policy=None  # don't destroy the bucket on deletion
        )

        # ✅ Save bucket name in SSM for other stacks to use
        ssm.StringParameter(
            self, "ModelArtifactBucketParam",
            parameter_name="/ml-pipeline/s3/model-artifact-bucket",
            string_value=self.artifact_bucket.bucket_name,
        )

        # 🔐 IAM Role for SageMaker to access S3
        self.sagemaker_role = iam.Role(
            self, "SageMakerExecutionRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
            ]
        )

        # ✅ Save role ARN in SSM
        ssm.StringParameter(
            self, "SageMakerExecutionRoleParam",
            parameter_name="/ml-pipeline/sagemaker/execution-role-arn",
            string_value=self.sagemaker_role.role_arn,
        )
