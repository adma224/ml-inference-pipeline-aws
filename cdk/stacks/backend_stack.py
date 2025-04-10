from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_ssm as ssm,
    Duration,
)
from constructs import Construct

class BackendStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 🧠 Generate Lambda: Sends prompt to SageMaker
        endpoint_param = ssm.StringParameter.from_string_parameter_name(
            self, "EndpointNameParam",
            string_parameter_name="/ml-pipeline/sagemaker/endpoint-name"
        )

        self.generate_fn = _lambda.Function(
            self, "GenerateHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("../lambda/generate"),
            environment={
                "ENDPOINT_NAME_PARAM": endpoint_param.parameter_name
            },
            timeout=Duration.seconds(30)
        )

        endpoint_param.grant_read(self.generate_fn)

        self.generate_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["sagemaker:InvokeEndpoint"],
                resources=["*"]
            )
        )

        # ✅ Ping Lambda: Warm-up check or health check
        self.ping_fn = _lambda.Function(
            self, "PingHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("../lambda/ping"),
            timeout=Duration.seconds(5)
        )

        # ✅ Flag Lambda: Save user feedback (placeholder)
        self.flag_fn = _lambda.Function(
            self, "FlagHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("../lambda/flag"),
            timeout=Duration.seconds(5)
        )
