from aws_cdk import (
    Stack,
    Duration,
    aws_ssm as ssm,
    aws_sagemaker as sagemaker,
    aws_cloudwatch as cw,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_applicationautoscaling as appscaling,
    aws_logs as logs,
    CfnOutput,
)
from constructs import Construct


class AIStack(Stack):
    """
    Real-time SageMaker endpoint with:
      - Data capture to S3
      - 5XX alarm to SNS
      - Autoscaling (variant-level) with min/max capacity
      - SageMaker log group retention (30d)
    """

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Inputs from SSM
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

        model_data_url = (
            f"s3://{bucket_param.string_value}/gpt2-v1/"
            f"{version_param.string_value}/model.tar.gz"
        )

        # Model
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

        # EndpointConfig (single variant "AllTraffic" + data capture)
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

        # Pre-create SageMaker endpoint log group with retention
        logs.LogGroup(
            self, "SageMakerEndpointLogs",
            log_group_name="/aws/sagemaker/Endpoints/gpt2-endpoint",
            retention=logs.RetentionDays.THIRTY_DAYS,
            removal_policy=None,
        )

        # Endpoint
        endpoint = sagemaker.CfnEndpoint(
            self, "Gpt2Endpoint",
            endpoint_name="gpt2-endpoint",
            endpoint_config_name=endpoint_config.attr_endpoint_config_name,
        )

        # Publish endpoint name to SSM
        ssm.StringParameter(
            self, "SageMakerEndpointParam",
            parameter_name="/ml-pipeline/sagemaker/endpoint-name",
            string_value=endpoint.endpoint_name,
        )

        CfnOutput(self, "SageMakerEndpointName", value=endpoint.endpoint_name)

        # Minimal alarm: Invocation 5XX -> SNS email
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

        # Autoscaling for the AllTraffic variant (min=1, max=2)
        resource_id = "endpoint/gpt2-endpoint/variant/AllTraffic"
        scalable_target = appscaling.ScalableTarget(
            self, "SageMakerVariantScalableTarget",
            service_namespace=appscaling.ServiceNamespace.SAGEMAKER,
            resource_id=resource_id,
            scalable_dimension="sagemaker:variant:DesiredInstanceCount",
            min_capacity=1,
            max_capacity=2,
        )
        scalable_target.scale_to_track_metric(
            "InvocationsPerInstancePolicy",
            predefined_metric=appscaling.PredefinedMetric.SAGEMAKER_VARIANT_INVOCATIONS_PER_INSTANCE,
            target_value=70.0,
            scale_in_cooldown=Duration.minutes(10),
            scale_out_cooldown=Duration.minutes(5),
        )
