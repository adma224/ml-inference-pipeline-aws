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

        # 🔐 Load endpoint param for Lambdas
        endpoint_param = ssm.StringParameter.from_string_parameter_name(
            self, "EndpointNameParam",
            string_parameter_name="/ml-pipeline/sagemaker/endpoint-name"
        )

        # 🧠 Lambda: Generate response from SageMaker
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

        # 🔄 Lambda: Ping endpoint with "__ping__"
        self.ping_fn = _lambda.Function(
            self, "PingHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("../lambda/ping"),
            environment={
                "ENDPOINT_NAME_PARAM": endpoint_param.parameter_name
            },
            timeout=Duration.seconds(30)
        )
        endpoint_param.grant_read(self.ping_fn)
        self.ping_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["sagemaker:InvokeEndpoint"],
                resources=["*"]
            )
        )

        # 👍 Lambda: Handle vote input (up/down)
        self.vote_fn = _lambda.Function(
            self, "VoteHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("../lambda/vote"),
            environment={
                "ENDPOINT_NAME_PARAM": endpoint_param.parameter_name
            },
            timeout=Duration.seconds(5)
        )
        endpoint_param.grant_read(self.vote_fn)
