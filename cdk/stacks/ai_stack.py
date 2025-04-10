from aws_cdk import (
    Stack,
    aws_ssm as ssm,
    aws_sagemaker as sagemaker,
    CfnOutput,
)
from constructs import Construct

class AIStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 🔹 Load required values from SSM
        bucket_param = ssm.StringParameter.from_string_parameter_name(
            self, "ModelArtifactBucket",
            string_parameter_name="/ml-pipeline/s3/model-artifact-bucket"
        )

        role_param = ssm.StringParameter.from_string_parameter_name(
            self, "SageMakerExecutionRole",
            string_parameter_name="/ml-pipeline/sagemaker/execution-role-arn"
        )

        version_param = ssm.StringParameter.from_string_parameter_name(
            self, "ModelVersion",
            string_parameter_name="/ml-pipeline/model/latest-version"
        )

        # 🔹 Construct full S3 path to model artifacts
        model_data_url = f"s3://{bucket_param.string_value}/gpt2-v1/{version_param.string_value}/model.tar.gz"

        # 🔹 Define SageMaker model resource
        model = sagemaker.CfnModel(
            self, "Gpt2Model",
            model_name="gpt2-model",
            execution_role_arn=role_param.string_value,
            primary_container={
                "image": "763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-inference:1.13.1-transformers4.26.0-cpu-py39-ubuntu20.04",
                "modelDataUrl": model_data_url
            }
        )

        # 🔹 Define endpoint configuration
        endpoint_config = sagemaker.CfnEndpointConfig(
            self, "Gpt2EndpointConfig",
            endpoint_config_name="gpt2-endpoint-config",
            production_variants=[{
                "modelName": model.attr_model_name,  # ensure dependency resolution
                "variantName": "AllTraffic",
                "serverlessConfig": {
                    "memorySizeInMb": 2048,
                    "maxConcurrency": 2
                }
            }]
        )

        # 🔹 Create the SageMaker endpoint
        endpoint = sagemaker.CfnEndpoint(
            self, "Gpt2Endpoint",
            endpoint_name="gpt2-endpoint",
            endpoint_config_name=endpoint_config.attr_endpoint_config_name
        )

        # 🔹 Save the endpoint name in SSM for Lambda usage
        ssm.StringParameter(self, "SageMakerEndpointParam",
            parameter_name="/ml-pipeline/sagemaker/endpoint-name",
            string_value=endpoint.endpoint_name
        )

        # Optional: Output the endpoint name for visibility
        CfnOutput(self, "SageMakerEndpointName",
            value=endpoint.endpoint_name
        )
