from aws_cdk import core
from aws_cdk import aws_dynamodb
from aws_cdk import aws_lambda
from aws_cdk import aws_apigateway

from deployment.components.aws_lambda.construct import CreateAnnouncementLambda


class AnnouncementAppStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.table = aws_dynamodb.Table(
            self,
            "Announcements",
            table_name="Announcements",
            partition_key=aws_dynamodb.Attribute(
                name="id", type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="date", type=aws_dynamodb.AttributeType.STRING
            ),
            read_capacity=5,
            write_capacity=5,
        )

        core.CfnOutput(self, "AnnouncementTableName", value=self.table.table_name)

        create_announcement_lambda = CreateAnnouncementLambda(
            self,
            "CreateAnnouncementLambda",
            {
                "lambda_config": {
                    "handler": "create_announcement.main",
                    "runtime": aws_lambda.Runtime.PYTHON_3_8,
                    "timeout": core.Duration.minutes(5),
                    "environment": {
                        "TABLE_NAME": self.table.table_name,
                    },
                    "retry_attempts": 0,
                },
            },
        ).function

        self.table.grant_read_write_data(create_announcement_lambda)

        api = aws_apigateway.LambdaRestApi(
            self,
            "AnnouncementAPI",
            handler=create_announcement_lambda,
            proxy=False,
            minimum_compression_size=10240,
            deploy_options=aws_apigateway.StageOptions(
                tracing_enabled=True, metrics_enabled=True
            ),
            default_cors_preflight_options={
                "allow_origins": aws_apigateway.Cors.ALL_ORIGINS,
                "allow_methods": ["GET", "POST", "OPTIONS"],
            },
        )
