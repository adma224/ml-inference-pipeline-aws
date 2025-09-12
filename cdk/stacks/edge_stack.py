from aws_cdk import (
    Stack, CfnOutput,
    aws_s3 as s3,
    aws_route53 as route53, aws_route53_targets as targets,
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_iam as iam,
    aws_ssm as ssm,
)
from constructs import Construct

DOMAIN = "adrianmurillo.io"  # MVP: hardcoded

class EdgeStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, *, website_bucket: s3.IBucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Hosted zone must already exist
        zone = route53.HostedZone.from_lookup(self, "Zone", domain_name=DOMAIN)

        # CloudFront cert (ACM in us-east-1)
        cert = acm.Certificate(
            self, "Cert",
            domain_name=DOMAIN,
            subject_alternative_names=[f"www.{DOMAIN}"],
            validation=acm.CertificateValidation.from_dns(zone),
        )

        # Origin Access Control
        oac = cloudfront.CfnOriginAccessControl(
            self, "OAC",
            origin_access_control_config=cloudfront.CfnOriginAccessControl.OriginAccessControlConfigProperty(
                name=f"{DOMAIN}-oac",
                origin_access_control_origin_type="s3",
                signing_behavior="always",
                signing_protocol="sigv4",
            )
        )

        # CloudFront -> S3 (REST origin)
        dist = cloudfront.Distribution(
            self, "Dist",
            certificate=cert,
            domain_names=[DOMAIN, f"www.{DOMAIN}"],
            default_root_object="index.html",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin(website_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
        )

        # Publish distribution ID for CI
        ssm.StringParameter(
            self, "EdgeDistributionId",
            parameter_name="/ml-pipeline/edge/distribution-id",
            string_value=dist.distribution_id,
        )

        # Attach OAC to origin (L1 override)
        dist_l1: cloudfront.CfnDistribution = dist.node.default_child  # type: ignore
        dist_l1.add_property_override(
            "DistributionConfig.Origins.0.OriginAccessControlId", oac.attr_id
        )

        # Bucket policy: allow only this distribution to read
        website_bucket.add_to_resource_policy(iam.PolicyStatement(
            sid="AllowCloudFrontReadViaOAC",
            actions=["s3:GetObject"],
            resources=[f"{website_bucket.bucket_arn}/*"],
            principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
            conditions={"StringEquals": {"AWS:SourceArn": dist.distribution_arn}},
        ))

        # DNS: apex + www -> CloudFront (A and AAAA)
        route53.ARecord(
            self, "AliasApex",
            zone=zone,
            record_name=DOMAIN,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(dist)),
        )
        route53.AaaaRecord(
            self, "AliasApexAAAA",
            zone=zone,
            record_name=DOMAIN,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(dist)),
        )

        route53.ARecord(
            self, "AliasWWW",
            zone=zone,
            record_name=f"www.{DOMAIN}",
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(dist)),
        )
        route53.AaaaRecord(
            self, "AliasWWWAAAA",
            zone=zone,
            record_name=f"www.{DOMAIN}",
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(dist)),
        )

        CfnOutput(self, "SiteURL", value=f"https://{DOMAIN}")
        CfnOutput(self, "CloudFrontDomain", value=dist.domain_name)
