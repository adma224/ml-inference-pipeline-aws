from aws_cdk import (
    Stack,
    aws_sagemaker as sagemaker,
    aws_ssm as ssm
)
from constructs import Construct

class InferenceStack(Stack):

    def __init__(self, scope: Construct, id: str, artifact_bucket, sagemaker_role, **kwargs):
        super().__init__(scope, id, **kwargs)

        model = sagemaker.CfnModel(
            self, "Gpt2Model",
            execution_role_arn=sagemaker_role.role_arn,
            primary_container={
                "image": "763104351884.dkr.ecr.us-west-2.amazonaws.com/pytorch-inference:2.1.1-cpu-py310-ubuntu20.04",
                "modelDataUrl": "s3://infrastack-modelartifactbucketf271bf2c-xgmpcko1h6hz/gpt2-v1/v20250328-235901/model.tar.gz"
            }
        )

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

        endpoint = sagemaker.CfnEndpoint(
            self, "Gpt2Endpoint",
            endpoint_config_name=endpoint_config.attr_endpoint_config_name
        )

        # ✅ Must happen *after* `endpoint` is defined
        ssm.StringParameter(self, "EndpointNameParam",
            parameter_name="/ml-pipeline/sagemaker/endpoint-name",
            string_value=endpoint.attr_endpoint_name
        )


