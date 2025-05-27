from aws_cdk import (
    Stack,
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_s3 as s3,
    CfnOutput
)
from aws_cdk.aws_s3_origins import S3Origin
from constructs import Construct  # not Constructs

class NetworkStack(Stack):
    def __init__(self, scope: Construct, id: str, frontend_bucket: s3.IBucket, **kwargs):
        super().__init__(scope, id, **kwargs)

        domain_name = "adrianmurillo.io"

        # 1. Look up the hosted zone
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name=domain_name
        )

        # 2. Create ACM certificate (must be in us-east-1)
        certificate = acm.Certificate(
            self, "SiteCertificate",
            domain_name=domain_name,
            validation=acm.CertificateValidation.from_dns(hosted_zone)
        )

        # 3. Create CloudFront distribution pointing to S3 bucket
        distribution = cloudfront.Distribution(
            self, "FrontendDistribution",
            default_root_object="index.html",
            domain_names=[domain_name],
            certificate=certificate,
            default_behavior=cloudfront.BehaviorOptions(
                origin=S3Origin(frontend_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            )
        )

        # 4. Create Route 53 alias record pointing to CloudFront
        route53.ARecord(
            self, "AliasRecord",
            zone=hosted_zone,
            record_name=domain_name,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution))
        )

        # 5. Output the CloudFront domain name
        CfnOutput(self, "CloudFrontURL", value=f"https://{distribution.domain_name}")
