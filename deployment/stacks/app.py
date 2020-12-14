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
    def __init__(
        self, scope: core.Construct, construct_id: str, *, settings, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = self.create_table(settings)

        api = self.create_app(settings)

        announcement_resource = AnnouncemenetResourceStack(
            self, api=api, table_name=table.table_name, settings=settings
        )

        deployment = self.deploy(api, methods=announcement_resource.methods)
        deployment.add_dependency(announcement_resource)

    def create_app(self, settings) -> aws_apigateway.RestApi:
        return aws_apigateway.RestApi(
            self,
            settings.AWS_API_GATEWAY_APP_NAME,
            # For now we do not want to keep old deployments
            retain_deployments=False,
            minimum_compression_size=10240,
            default_cors_preflight_options={
                "allow_origins": settings.CORS_ALLOWED_ORIGINS.split(","),
                "allow_methods": ["GET", "POST", "OPTIONS"],
            },
            # Because deployment is made by another stack,
            # we have to prevent deploying this API
            deploy=False,
        )

    def create_table(self, settings) -> aws_dynamodb.Table:
        return create_table(
            self,
            {
                "read_capacity": settings.AWS_DYNAMODB_READ_CAPACITY,
                "write_capacity": settings.AWS_DYNAMODB_WRITE_CAPACITY,
                "table_name": settings.AWS_DYNAMODB_TABLE_NAME,
            },
        )


class AnnouncementAppProdStack(AnnouncementAppStack):
    def deploy(
        self, api: aws_apigateway.RestApi, methods: List[aws_apigateway.Method]
    ) -> APIProdDeploymentStack:
        return APIProdDeploymentStack(
            self,
            rest_api_id=api.rest_api_id,
            root_resource_id=api.root.resource_id,
            methods=methods,
        )


class AnnouncementAppDevStack(AnnouncementAppStack):
    def deploy(
        self, api: aws_apigateway.RestApi, methods: List[aws_apigateway.Method]
    ) -> APIDevDeploymentStack:
        return APIDevDeploymentStack(
            self,
            rest_api_id=api.rest_api_id,
            root_resource_id=api.root.resource_id,
            methods=methods,
        )