from aws_cdk import (
    Stack,
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    CfnOutput,
)
from aws_cdk.aws_cloudfront_origins import S3StaticWebsiteOrigin
from constructs import Construct


class NetworkStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        frontend_bucket: s3.IBucket,
        rest_api: apigateway.IRestApi,
        domain_name: str,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        root_domain = domain_name
        api_subdomain = f"api.{root_domain}"

        # 1) Public hosted zone (create one; if you already have one, switch to HostedZone.from_lookup)
        hosted_zone = route53.PublicHostedZone(self, "HostedZone", zone_name=root_domain)

        # 2) Certificates
        #    NOTE: For CloudFront, the cert must be in us-east-1. If your app is deployed elsewhere,
        #    consider creating this certificate in a separate, us-east-1-targeted stack.
        site_cert = acm.Certificate(
            self, "SiteCertificate",
            domain_name=root_domain,
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )
        api_cert = acm.Certificate(
            self, "ApiCertificate",
            domain_name=api_subdomain,
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )

        # 3) CloudFront distribution for the static site (S3 website origin)
        distribution = cloudfront.Distribution(
            self, "FrontendDistribution",
            default_root_object="index.html",
            domain_names=[root_domain],
            certificate=site_cert,  # <- use the site cert
            default_behavior=cloudfront.BehaviorOptions(
                origin=S3StaticWebsiteOrigin(frontend_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
        )

        # 4) Route53 A-record for the website root -> CloudFront
        route53.ARecord(
            self, "SiteAliasRecord",
            zone=hosted_zone,
            record_name=root_domain,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)),
        )

        # 5) API custom domain: api.<root_domain> -> API Gateway (Regional)
        api_domain = apigateway.DomainName(
            self, "ApiCustomDomain",
            domain_name=api_subdomain,
            certificate=api_cert,
            endpoint_type=apigateway.EndpointType.REGIONAL,
            security_policy=apigateway.SecurityPolicy.TLS_1_2,
        )

        # Base path mapping: map the custom domain root to the REST API prod stage
        apigateway.BasePathMapping(
            self, "ApiBasePathMapping",
            domain_name=api_domain,
            rest_api=rest_api,
            stage=rest_api.deployment_stage,
        )

        # 6) Route53 A-record for api subdomain -> API Gateway custom domain
        route53.ARecord(
            self, "ApiAliasRecord",
            zone=hosted_zone,
            record_name=api_subdomain,
            target=route53.RecordTarget.from_alias(targets.ApiGatewayDomain(api_domain)),
        )

        # Outputs
        CfnOutput(self, "CloudFrontURL", value=f"https://{distribution.domain_name}")
        CfnOutput(self, "SiteURL", value=f"https://{root_domain}")
        CfnOutput(self, "ApiURL", value=f"https://{api_subdomain}")

