from aws_cdk import (
    Stack,
    aws_sagemaker as sagemaker,
    aws_ssm as ssm
)
from constructs import Construct

class InferenceStack(Stack):

    def __init__(self, scope: Construct, id: str, artifact_bucket_name: str, sagemaker_role_arn: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 🔹 Retrieve the latest model version from SSM
        version_param = ssm.StringParameter.from_string_parameter_name(
            self, "ModelVersionTagParam",
            string_parameter_name="/ml-pipeline/model/latest-version"
        )

        # 🔹 Construct full model S3 path using the bucket name and SSM version tag
        model_data_url = f"s3://{artifact_bucket_name}/gpt2-v1/{version_param.string_value}/model.tar.gz"

        # 🔹 Generate model name and config name
        model_name = "gpt2-model"
        endpoint_config_name = "gpt2-endpoint-config"
        endpoint_name = "gpt2-endpoint"

        # 🔹 Define the SageMaker model
        model = sagemaker.CfnModel(
            self, "Gpt2Model",
            model_name=model_name,
            execution_role_arn=sagemaker_role_arn,
            primary_container={
                "image": "763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-inference:1.13.1-transformers4.26.0-cpu-py39-ubuntu20.04",
                "modelDataUrl": model_data_url
            }
        )

        # 🔹 Define the endpoint config
        endpoint_config = sagemaker.CfnEndpointConfig(
            self, "Gpt2EndpointConfig",
            endpoint_config_name=endpoint_config_name,
            production_variants=[{
                "modelName": model.attr_model_name,
                "variantName": "AllTraffic",
                "serverlessConfig": {
                    "memorySizeInMb": 2048,
                    "maxConcurrency": 2
                }
            }]
        )

        # 🔹 Create the endpoint
        endpoint = sagemaker.CfnEndpoint(
            self, "Gpt2Endpoint",
            endpoint_name=endpoint_name,
            endpoint_config_name=endpoint_config.attr_endpoint_config_name
        )

        # 🔹 Store names in SSM for other stacks to use
        ssm.StringParameter(self, "ModelNameParam",
            parameter_name="/ml-pipeline/sagemaker/model-name",
            string_value=model_name
        )

        ssm.StringParameter(self, "ModelConfigNameParam",
            parameter_name="/ml-pipeline/sagemaker/config-name",
            string_value=endpoint_config_name
        )

        ssm.StringParameter(self, "EndpointNameParam",
            parameter_name="/ml-pipeline/sagemaker/endpoint-name",
            string_value=endpoint_name
        )
