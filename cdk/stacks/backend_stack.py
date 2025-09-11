from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    CfnResource, RemovalPolicy
)
from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import CfnOutput
from aws_cdk import aws_rds as rds

from constructs import Construct


class BackendStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # --- VPC --------------------------------------------------------------
        vpc = ec2.Vpc(self, "BackendVpc", max_azs=2)

        # --- Aurora Serverless v2 (high-level) --------------------------------
        # Using high-level ServerlessCluster so we get .cluster_arn and .secret
        cluster = rds.DatabaseCluster(
            self, "AuroraServerlessV2",
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.VER_15_3
            ),
            writer=rds.ClusterInstance.serverless_v2("writer"),
            readers=[rds.ClusterInstance.serverless_v2("reader1")],
            vpc=vpc,
            default_database_name="ml_pipeline_response_data",
            removal_policy=RemovalPolicy.DESTROY
        )


        db_secret = cluster.secret


        # --- IAM policy for RDS Data API + Secrets ----------------------------
        rds_access_policy = iam.PolicyStatement(
            actions=["rds-data:*", "secretsmanager:GetSecretValue"],
            resources=["*"]
        )

        # --- SSM: SageMaker endpoint name (define BEFORE Lambdas that use it) --
        endpoint_param = ssm.StringParameter.from_string_parameter_name(
            self, "EndpointNameParam",
            string_parameter_name="/ml-pipeline/sagemaker/endpoint-name"
        )

        # --- DBInitHandler (does NOT need SageMaker endpoint) ------------------
        db_init_fn = _lambda.Function(
            self, "DBInitHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("../lambda/db_init"),
            vpc=vpc,
            timeout=Duration.seconds(30),
            environment={
                "CLUSTER_ARN": cluster.cluster_arn,
                "DB_SECRET_ARN": db_secret.secret_arn,
                "DB_NAME": "mlpipeline"
            }
        )
        db_init_fn.add_to_role_policy(rds_access_policy)

        # Trigger DB init once the stack is deployed
        CfnResource(self, "DBInitTrigger",
            type="Custom::DBInit",
            properties={"ServiceToken": db_init_fn.function_arn}
        )

        # --- GenerateHandler (needs SageMaker + DB) ----------------------------
        self.generate_fn = _lambda.Function(
            self, "GenerateHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("../lambda/generate"),
            vpc=vpc,
            timeout=Duration.seconds(30),
            environment={
                "ENDPOINT_NAME_PARAM": endpoint_param.parameter_name,
                "CLUSTER_ARN": cluster.cluster_arn,
                "DB_SECRET_ARN": db_secret.secret_arn,
                "DB_NAME": "mlpipeline"
            }
        )
        endpoint_param.grant_read(self.generate_fn)
        self.generate_fn.add_to_role_policy(rds_access_policy)
        self.generate_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["sagemaker:InvokeEndpoint"],
            resources=["*"]
        ))

        # --- PingHandler (needs SageMaker only) --------------------------------
        self.ping_fn = _lambda.Function(
            self, "PingHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("../lambda/ping"),
            vpc=vpc,
            timeout=Duration.seconds(30),
            environment={
                "ENDPOINT_NAME_PARAM": endpoint_param.parameter_name
            }
        )
        endpoint_param.grant_read(self.ping_fn)
        self.ping_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["sagemaker:InvokeEndpoint"],
            resources=["*"]
        ))

        # --- VoteHandler (DB only) --------------------------------------------
        self.vote_fn = _lambda.Function(
            self, "VoteHandler",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=_lambda.Code.from_asset("../lambda/vote"),
            vpc=vpc,
            timeout=Duration.seconds(5),
            environment={
                "CLUSTER_ARN": cluster.cluster_arn,
                "DB_SECRET_ARN": db_secret.secret_arn,
                "DB_NAME": "mlpipeline"
            }
        )
        self.vote_fn.add_to_role_policy(rds_access_policy)

        # --- SSM outputs (optional) -------------------------------------------
        ssm.StringParameter(self, "AuroraClusterArnParam",
            parameter_name="/ml-pipeline/db/cluster-arn",
            string_value=cluster.cluster_arn
        )
        ssm.StringParameter(self, "AuroraSecretArnParam",
            parameter_name="/ml-pipeline/db/secret-arn",
            string_value=db_secret.secret_arn
        )

        CfnOutput(self, "DbClusterArn", value=cluster.cluster_arn)
        CfnOutput(self, "DbSecretArn", value=db_secret.secret_arn)
