# stacks/ai_stack.py
from aws_cdk import (
    Stack,
    Duration,
    aws_ssm as ssm,
    aws_sagemaker as sagemaker,
    aws_cloudwatch as cw,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    CfnOutput,
)
from constructs import Construct


class AIStack(Stack):
    """
    Hosts the active real-time SageMaker endpoint used by the app.

    Responsibilities
    - Read shared settings from SSM (artifact bucket, execution role, model version).
    - Create CfnModel -> points to model.tar.gz in S3 and uses your execution role.
    - Create CfnEndpointConfig -> real-time instance + data capture to S3.
    - Create CfnEndpoint -> stable name "gpt2-endpoint".
    - Publish endpoint name to SSM for Lambda to consume.
    - Wire a minimal 5XX CloudWatch Alarm to SNS (email).

    Notes
    - If data capture files do not appear in S3, add an S3 bucket policy that allows
      PutObject from the SageMaker service principal to the capture prefix.
    """

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # ----- Inputs pulled from SSM (created by BaseStack) -----
        bucket_param = ssm.StringParameter.from_string_parameter_name(
            self, "ModelArtifactBucket",
            string_parameter_name="/ml-pipeline/s3/model-artifact-bucket",
        )
        role_param = ssm.StringParameter.from_string_parameter_name(
            self, "SageMakerExecutionRole",
            string_parameter_name="/ml-pipeline/sagemaker/execution-role-arn",
        )
        version_param = ssm.StringParameter.from_string_parameter_name(
            self, "ModelVersion",
            string_parameter_name="/ml-pipeline/model/latest-version",
        )

        # Model artifact location: s3://<bucket>/gpt2-v1/<version>/model.tar.gz
        model_data_url = (
            f"s3://{bucket_param.string_value}/gpt2-v1/"
            f"{version_param.string_value}/model.tar.gz"
        )

        # ----- CfnModel (container image + model data + execution role) -----
        model = sagemaker.CfnModel(
            self, "Gpt2Model",
            model_name="gpt2-model",
            execution_role_arn=role_param.string_value,
            primary_container={
                "image": (
                    "763104351884.dkr.ecr.us-east-1.amazonaws.com/"
                    "huggingface-pytorch-inference:1.13.1-transformers4.26.0-cpu-py39-ubuntu20.04"
                ),
                "modelDataUrl": model_data_url,
            },
        )

        # ----- CfnEndpointConfig (real-time instance + data capture) -----
        # Real-time: single small CPU instance to keep costs down for demos.
        # Data capture: 100% of requests/responses to s3://<bucket>/gpt2-v1/data-capture/
        endpoint_config = sagemaker.CfnEndpointConfig(
            self, "Gpt2EndpointConfig",
            endpoint_config_name="gpt2-endpoint-config",
            production_variants=[{
                "modelName": model.attr_model_name,
                "variantName": "AllTraffic",
                "initialInstanceCount": 1,
                "instanceType": "ml.m5.large",
            }],
            data_capture_config=sagemaker.CfnEndpointConfig.DataCaptureConfigProperty(
                enable_capture=True,
                initial_sampling_percentage=100,
                destination_s3_uri=f"s3://{bucket_param.string_value}/gpt2-v1/data-capture/",
                capture_options=[
                    sagemaker.CfnEndpointConfig.CaptureOptionProperty(capture_mode="Input"),
                    sagemaker.CfnEndpointConfig.CaptureOptionProperty(capture_mode="Output"),
                ],
                capture_content_type_header=sagemaker.CfnEndpointConfig.CaptureContentTypeHeaderProperty(
                    csv_content_types=["text/csv"],
                    json_content_types=["application/json"],
                ),
            ),
        )

        # ----- CfnEndpoint (stable endpoint name) -----
        endpoint = sagemaker.CfnEndpoint(
            self, "Gpt2Endpoint",
            endpoint_name="gpt2-endpoint",
            endpoint_config_name=endpoint_config.attr_endpoint_config_name,
        )

        # Publish endpoint name to SSM for Lambda (BackendStack) to read at runtime
        ssm.StringParameter(
            self, "SageMakerEndpointParam",
            parameter_name="/ml-pipeline/sagemaker/endpoint-name",
            string_value=endpoint.endpoint_name,
        )

        CfnOutput(self, "SageMakerEndpointName", value=endpoint.endpoint_name)

        # ----- Minimal monitoring: 5XX errors -> SNS email -----
        topic = sns.Topic(self, "SageMakerAlarms")
        topic.add_subscription(subs.EmailSubscription("adrianmurilloaraya@gmail.com"))

        error_metric = cw.Metric(
            namespace="AWS/SageMaker",
            metric_name="Invocation5XXErrors",
            dimensions_map={"EndpointName": "gpt2-endpoint", "VariantName": "AllTraffic"},
            statistic="Sum",
            period=Duration.minutes(1),
        )

        cw.Alarm(
            self, "Endpoint5XXAlarm",
            metric=error_metric,
            threshold=1,
            evaluation_periods=1,
            comparison_operator=cw.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
        ).add_alarm_action(cw_actions.SnsAction(topic))

