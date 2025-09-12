from aws_cdk import (
    Stack, RemovalPolicy, CfnOutput,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_apigateway as apigateway,
    aws_ssm as ssm,
)
from constructs import Construct

class FrontendStack(Stack):
    def __init__(self, scope: Construct, id: str, *,
                 generate_fn, ping_fn, vote_fn,
                 bucket_name: str | None = None,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Private, deterministic bucket (name must be globally unique if provided)
        self.frontend_bucket = s3.Bucket(
            self, "FrontendBucket",
            bucket_name=bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Publish bucket name for CI
        ssm.StringParameter(
            self, "FrontendBucketParam",
            parameter_name="/ml-pipeline/frontend/bucket-name",
            string_value=self.frontend_bucket.bucket_name,
        )

        # Upload static assets
        s3_deployment.BucketDeployment(
            self, "FrontendDeployment",
            sources=[s3_deployment.Source.asset("../web_pages")],
            destination_bucket=self.frontend_bucket,
        )

        # REST API (Regional) with simple CORS
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

        self.api.root.add_resource("generate") \
            .add_method("POST", apigateway.LambdaIntegration(generate_fn, proxy=True))
        self.api.root.add_resource("ping") \
            .add_method("GET", apigateway.LambdaIntegration(ping_fn, proxy=True))
        self.api.root.add_resource("vote") \
            .add_method("POST", apigateway.LambdaIntegration(vote_fn, proxy=True))

        # Publish API base URL (optional convenience)
        ssm.StringParameter(
            self, "ApiUrlParam",
            parameter_name="/ml-pipeline/api/url",
            string_value=self.api.url,
        )

        # Outputs (single, non-duplicated)
        CfnOutput(self, "FrontendBucketName", value=self.frontend_bucket.bucket_name)
        CfnOutput(self, "ApiGatewayURL", value=self.api.url)
