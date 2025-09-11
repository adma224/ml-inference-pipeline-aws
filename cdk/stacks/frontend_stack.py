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


from aws_cdk import aws_route53 as route53
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk.aws_s3_origins import S3Origin
from aws_cdk import aws_route53_targets as targets




from constructs import Construct

class FrontendStack(Stack):
    def __init__(self, scope: Construct, id: str, generate_fn, ping_fn, vote_fn, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket for static website hosting.
        frontend_bucket = s3.Bucket(self, "FrontendBucket",
            website_index_document="index.html",
            website_error_document="error.html",
            public_read_access=True,
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

        # Assume frontend_bucket is already created (you have it)

        # Hosted Zone
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name="adrianmurillo.io"
        )

        # Certificate
        certificate = acm.Certificate(
            self, "SiteCertificate",
            domain_name="adrianmurillo.io",
            validation=acm.CertificateValidation.from_dns(hosted_zone)
        )

        # CloudFront Distribution
        distribution = cloudfront.Distribution(
            self, "FrontendDistribution",
            default_root_object="index.html",
            domain_names=["adrianmurillo.io"],
            certificate=certificate,
            default_behavior=cloudfront.BehaviorOptions(
                origin=S3Origin(frontend_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            )
        )

        # Route53 Alias Record
        route53.ARecord(
            self, "AliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)),
            record_name="adrianmurillo.io"
        )



        # Define the API Gateway
        api = apigateway.RestApi(
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

        # Then just attach Lambdas with proxy integration:
        generate = api.root.add_resource("generate")
        generate.add_method("POST", apigateway.LambdaIntegration(generate_fn, proxy=True))

        ping = api.root.add_resource("ping")
        ping.add_method("GET", apigateway.LambdaIntegration(ping_fn, proxy=True))

        vote = api.root.add_resource("vote")
        vote.add_method("POST", apigateway.LambdaIntegration(vote_fn, proxy=True))

        # Save the API URL to SSM for other stacks or services to reference
        ssm.StringParameter(self, "ApiUrlParam",
            string_value=api.url,
            parameter_name="/ml-pipeline/api/url"
        )

        # Outputs for easy access
        CfnOutput(self, "FrontendBucketName", value=frontend_bucket.bucket_name)
        CfnOutput(self, "FrontendBucketWebsiteURL", value=frontend_bucket.bucket_website_url)
        CfnOutput(self, "ApiGatewayURL", value=api.url)
