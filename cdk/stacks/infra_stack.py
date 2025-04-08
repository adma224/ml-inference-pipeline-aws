from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_ssm as ssm,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.artifact_bucket = s3.Bucket(
            self, "ModelArtifactBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=True
        )

        # Save bucket name to SSM
        ssm.StringParameter(self, "ModelArtifactBucketNameParam",
            parameter_name="/ml-pipeline/s3/model-artifact-bucket",
            string_value=self.artifact_bucket.bucket_name
        )

        # Output for visibility
        CfnOutput(self, "ArtifactBucketName", value=self.artifact_bucket.bucket_name)

        self.sagemaker_role = iam.Role(
            self, "SageMakerExecutionRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess")
            ]
        )


