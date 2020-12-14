from typing import List

from aws_cdk import core
from aws_cdk import aws_dynamodb
from aws_cdk import aws_lambda
from aws_cdk import aws_apigateway

# from deployment.components.aws_lambda.function import AnnouncementLambda
from deployment.components.dynamodb.table import create_table
from deployment.components.aws_lambda.function import create_function
from deployment.stacks.api.announcement.resource import AnnouncemenetResourceStack
from deployment.stacks.api_deployment import (
    APIProdDeploymentStack,
    APIDevDeploymentStack,
)


class AnnouncementAppStack(core.Stack):
    CORS_ALLOWED_ORIGINS = ["*"]

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = self.create_table()

        api = self.create_app("AnnouncementAPI")

        announcement_resource = AnnouncemenetResourceStack(
            self,
            api=api,
            table_name=table.table_name,
        )

        deployment = self.deploy(api, methods=announcement_resource.methods)
        deployment.add_dependency(announcement_resource)

    def create_app(self, name: str):
        return aws_apigateway.RestApi(
            self,
            name,
            # For now we do not want to keep old deployments
            retain_deployments=False,
            minimum_compression_size=10240,
            default_cors_preflight_options={
                "allow_origins": self.CORS_ALLOWED_ORIGINS,
                "allow_methods": ["GET", "POST", "OPTIONS"],
            },
            # Because deployment is made by another stack,
            # we have to prevent deploying this API
            deploy=False,
        )


class AnnouncementAppProdStack(AnnouncementAppStack):
    CORS_ALLOWED_ORIGINS = ""

    def create_app(self, name: str):
        return super().create_app("Prod-AnnouncementAPI")

    def create_table(self):
        return create_table(
            self,
            {
                "read_capacity": 5,
                "write_capacity": 5,
                "table_name": "Prod-Announcement",
            },
        )

    def deploy(self, api: aws_apigateway.RestApi, methods: List[aws_apigateway.Method]):
        return APIProdDeploymentStack(
            self,
            rest_api_id=api.rest_api_id,
            root_resource_id=api.root.resource_id,
            methods=methods,
        )


class AnnouncementAppDevStack(AnnouncementAppStack):
    CORS_ALLOWED_ORIGINS = aws_apigateway.Cors.ALL_ORIGINS

    def create_app(self, name: str):
        return super().create_app("Dev-AnnouncementAPI")

    def create_table(self):
        return create_table(
            self,
            {"read_capacity": 5, "write_capacity": 5, "table_name": "Dev-Announcement"},
        )

    def deploy(self, api: aws_apigateway.RestApi, methods: List[aws_apigateway.Method]):
        return APIDevDeploymentStack(
            self,
            rest_api_id=api.rest_api_id,
            root_resource_id=api.root.resource_id,
            methods=methods,
        )