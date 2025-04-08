from aws_cdk import (
    Stack,
    aws_ssm as ssm,
    aws_sagemaker as sagemaker,
)
from constructs import Construct

class InferenceStack(Stack):

    def __init__(self, scope: Construct, id: str, artifact_bucket, sagemaker_role, **kwargs):
        super().__init__(scope, id, **kwargs)  # ✅ Don't pass custom args here
        # Get model artifact bucket name from SSM
        bucket_param = ssm.StringParameter.from_string_parameter_name(
            self, "ModelArtifactBucketNameParam",
            string_parameter_name="/ml-pipeline/s3/model-artifact-bucket"
        )

        # Get latest version tag from SSM
        version_param = ssm.StringParameter.from_string_parameter_name(
            self, "ModelVersionTagParam",
            string_parameter_name="/ml-pipeline/model/latest-version"
        )

        # Construct full model S3 path
        model_data_url = f"s3://{bucket_param.string_value}/gpt2-v1/{version_param.string_value}/model.tar.gz"

        # Define the SageMaker model
        model = sagemaker.CfnModel(
            self, "Gpt2Model",
            execution_role_arn=sagemaker_role.role_arn,
            primary_container={
                "image": "763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-inference:1.13.1-transformers4.26.0-cpu-py39-ubuntu20.04",
                "modelDataUrl": model_data_url
            }
        )

        # Define the endpoint config
        endpoint_config = sagemaker.CfnEndpointConfig(
            self, "Gpt2EndpointConfig",
            production_variants=[{
                "modelName": model.attr_model_name,
                "variantName": "AllTraffic",
                "serverlessConfig": {
                    "memorySizeInMb": 2048,
                    "maxConcurrency": 2
                }
            }]
        )

        # Create the endpoint
        endpoint = sagemaker.CfnEndpoint(
            self, "Gpt2Endpoint",
            endpoint_config_name=endpoint_config.attr_endpoint_config_name
        )

        # Store endpoint name in SSM for Lambda or frontend access
        ssm.StringParameter(self, "EndpointNameParam",
            parameter_name="/ml-pipeline/sagemaker/endpoint-name",
            string_value=endpoint.attr_endpoint_name
        )


