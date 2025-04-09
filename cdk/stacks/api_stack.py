from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_ssm as ssm,
    Duration
)
from constructs import Construct

class ApiStack(Stack):

    def __init__(self, scope: Construct, id: str, endpoint_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Load the parameter from SSM
        endpoint_param = ssm.StringParameter.from_string_parameter_name(
            self, "EndpointNameParam",
            string_parameter_name="/ml-pipeline/sagemaker/endpoint-name"
        )

        # Lambda Function
        invoke_lambda = _lambda.Function(
            self, "InvokeSageMakerEndpointHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("../lambda/invoke_endpoint"),
            environment={
                "ENDPOINT_NAME_PARAM": endpoint_param.parameter_name
            },
            timeout=Duration.seconds(30), 
        )

        # ✅ Grant the Lambda permission to read the SSM parameter
        endpoint_param.grant_read(invoke_lambda)


        # 2. Grant Lambda permission to call SageMaker endpoint
        invoke_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["sagemaker:InvokeEndpoint"],
                resources=["*"]  # Can be tightened by ARN if needed
            )
        )

        # 3. Create the REST API with rate limiting (no API key required)
        api = apigw.RestApi(self, "MLInferenceAPI",
            rest_api_name="ML Inference Service",
            deploy_options=apigw.StageOptions(
                throttling_rate_limit=5,
                throttling_burst_limit=2
            )
        )

        # 4. Add the /generate POST route
        resource = api.root.add_resource("generate")
        resource.add_method(
            "POST",
            apigw.LambdaIntegration(invoke_lambda),
            method_responses=[apigw.MethodResponse(status_code="200")],
            authorization_type=apigw.AuthorizationType.NONE
        )

        # After creating the API
        ssm.StringParameter(self, "ApiUrlParam",
            parameter_name="/ml-pipeline/api/url",
            string_value=f"https://{api.rest_api_id}.execute-api.{self.region}.amazonaws.com/{api.deployment_stage.stage_name}/generate"
        )
