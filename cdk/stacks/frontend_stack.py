from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_apigateway as apigateway,
    aws_ssm as ssm,
    aws_iam as iam,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct

class FrontendStack(Stack):
    def __init__(self, scope: Construct, id: str, generate_fn, ping_fn, vote_fn, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 1) Public website bucket (dev baseline)
        self.frontend_bucket = s3.Bucket(
            self, "FrontendBucket",
            website_index_document="index.html",
            website_error_document="error.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(block_public_policy=False),
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
        )
        self.frontend_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"{self.frontend_bucket.bucket_arn}/*"],
                principals=[iam.AnyPrincipal()],
            )
        )

        # 2) Deploy static assets
        s3_deployment.BucketDeployment(
            self, "FrontendDeployment",
            sources=[s3_deployment.Source.asset("../web_pages")],
            destination_bucket=self.frontend_bucket,
        )

        # 3) REST API (proxy + built-in CORS)
        self.api = apigateway.RestApi(
            self, "MLFrontendApi",
            rest_api_name="MLFrontendApi",
            deploy_options=apigateway.StageOptions(
                stage_name="prod",
                throttling_rate_limit=100.0,
                throttling_burst_limit=200,
            ),
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=["GET", "POST", "OPTIONS"],
                allow_headers=["Content-Type"],
            ),
        )

        generate = self.api.root.add_resource("generate")
        generate.add_method("POST", apigateway.LambdaIntegration(generate_fn, proxy=True))

        ping = self.api.root.add_resource("ping")
        ping.add_method("GET", apigateway.LambdaIntegration(ping_fn, proxy=True))

        vote = self.api.root.add_resource("vote")
        vote.add_method("POST", apigateway.LambdaIntegration(vote_fn, proxy=True))

        # 4) Expose the API base URL for the frontend (SSM)
        ssm.StringParameter(
            self, "ApiUrlParam",
            parameter_name="/ml-pipeline/api/url",
            string_value=self.api.url,  # e.g., https://<id>.execute-api.<region>.amazonaws.com/prod/
        )

        # 5) Outputs
        CfnOutput(self, "FrontendBucketName", value=self.frontend_bucket.bucket_name)
        CfnOutput(self, "FrontendBucketWebsiteURL", value=self.frontend_bucket.bucket_website_url)
        CfnOutput(self, "ApiGatewayURL", value=self.api.url)
