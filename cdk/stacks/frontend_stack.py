from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_apigateway as apigateway,
    aws_ssm as ssm,
    aws_iam as iam,
    CfnOutput,
    RemovalPolicy
)
from constructs import Construct

class FrontendStack(Stack):
    def __init__(self, scope: Construct, id: str, generate_fn, ping_fn, vote_fn, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket for static website hosting.
        frontend_bucket = s3.Bucket(self, "FrontendBucket",
            website_index_document="index.html",
            website_error_document="error.html",
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess(block_public_policy=False),
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        frontend_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"{frontend_bucket.bucket_arn}/*"],
                principals=[iam.AnyPrincipal()]
            )
        )

        s3_deployment.BucketDeployment(self, "FrontendDeployment",
            sources=[s3_deployment.Source.asset("../web_pages")],
            destination_bucket=frontend_bucket
        )

        # Define the API Gateway
        api = apigateway.RestApi(self, "MLFrontendApi",
            rest_api_name="MLFrontendApi",
            deploy_options=apigateway.StageOptions(stage_name="prod")
        )

        def add_cors_options(resource):
            resource.add_method(
                "OPTIONS",
                apigateway.MockIntegration(
                    integration_responses=[{
                        "statusCode": "200",
                        "responseParameters": {
                            "method.response.header.Access-Control-Allow-Headers": "'Content-Type'",
                            "method.response.header.Access-Control-Allow-Origin": "'*'",
                            "method.response.header.Access-Control-Allow-Methods": "'OPTIONS,POST,GET'",
                        }
                    }],
                    passthrough_behavior=apigateway.PassthroughBehavior.NEVER,
                    request_templates={"application/json": '{"statusCode": 200}'}
                ),
                method_responses=[{
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Headers": True,
                        "method.response.header.Access-Control-Allow-Origin": True,
                        "method.response.header.Access-Control-Allow-Methods": True,
                    }
                }]
            )

        def add_lambda_method(resource, method, fn):
            resource.add_method(method,
                apigateway.LambdaIntegration(fn, integration_responses=[{
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Origin": "'*'",
                        "method.response.header.Access-Control-Allow-Headers": "'Content-Type'",
                        "method.response.header.Access-Control-Allow-Methods": "'OPTIONS,POST,GET'"
                    }
                }]),
                method_responses=[{
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Origin": True,
                        "method.response.header.Access-Control-Allow-Headers": True,
                        "method.response.header.Access-Control-Allow-Methods": True
                    }
                }]
            )

        # API resources and their integrations
        generate = api.root.add_resource("generate")
        add_cors_options(generate)
        add_lambda_method(generate, "POST", generate_fn)

        ping = api.root.add_resource("ping")
        add_cors_options(ping)
        add_lambda_method(ping, "GET", ping_fn)

        vote = api.root.add_resource("vote")
        add_cors_options(vote)
        add_lambda_method(vote, "POST", vote_fn)

        # Security: Add Usage Plan for rate limiting
        usage_plan = apigateway.UsagePlan(self, "UsagePlan",
            name="RateLimitedUsagePlan",
            throttle={
                "burst_limit": 200,
                "rate_limit": 100
            }
        )
        # Attach the deployment stage to the usage plan so throttling applies
        usage_plan.add_api_stage(stage=api.deployment_stage)


        # Save the API URL to SSM for other stacks or services to reference
        ssm.StringParameter(self, "ApiUrlParam",
            string_value=api.url,
            parameter_name="/ml-pipeline/api/url"
        )

        # Outputs for easy access
        CfnOutput(self, "FrontendBucketName", value=frontend_bucket.bucket_name)
        CfnOutput(self, "FrontendBucketWebsiteURL", value=frontend_bucket.bucket_website_url)
        CfnOutput(self, "ApiGatewayURL", value=api.url)
