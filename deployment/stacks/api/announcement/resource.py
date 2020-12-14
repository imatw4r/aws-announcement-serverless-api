from aws_cdk import core
from aws_cdk import aws_apigateway
from aws_cdk import aws_dynamodb
from aws_cdk import aws_lambda


from deployment.components.aws_lambda.function import create_function


class AnnouncemenetResourceStack(core.NestedStack):
    def __init__(
        self,
        scope,
        *,
        api,
        table_name,
        parameters=None,
        timeout=None,
        notificationArns=None
    ):
        super().__init__(
            scope,
            "AnnouncemenetResourceStack",
            parameters=parameters,
            timeout=timeout,
            notification_arns=notificationArns,
        )
        self.methods = []

        announcement_resource = api.root.add_resource(
            "announcement",
        )

        table = aws_dynamodb.Table.from_table_name(self, "Table", table_name)

        self.add_post_method(api, resource=announcement_resource, table=table)
        self.add_get_method(api, resource=announcement_resource, table=table)

    def add_post_method(
        self,
        api: aws_apigateway.RestApi,
        resource: aws_apigateway.Resource,
        table: aws_dynamodb.Table,
    ) -> aws_apigateway.Method:
        create_announcement_lambda = create_function(
            stack=self,
            id="CreateAnnouncementLambda",
            settings={
                "handler": "create_announcement.main",
                "runtime": aws_lambda.Runtime.PYTHON_3_8,
                "timeout": core.Duration.minutes(5),
                "retry_attempts": 0,
            },
        )
        create_announcement_lambda.add_environment(
            "TABLE_NAME",
            table.table_name,
        )

        table.grant_read_write_data(create_announcement_lambda)

        create_announcement_request_validator = aws_apigateway.RequestValidator(
            self,
            "CreateAnnouncementRequestValidator",
            rest_api=api,
            validate_request_body=True,
            request_validator_name="Create Announcement Request Validator",
        )

        create_announcement_request_model = aws_apigateway.Model(
            self,
            "CreateAnnouncementRequestModel",
            model_name="CreateAnnouncementRequest",
            rest_api=api,
            schema=aws_apigateway.JsonSchema(
                type=aws_apigateway.JsonSchemaType.OBJECT,
                required=["Item"],
                properties={
                    "Item": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.OBJECT,
                        required=["title", "date", "description"],
                        properties={
                            "title": aws_apigateway.JsonSchema(
                                type=aws_apigateway.JsonSchemaType.STRING
                            ),
                            "description": aws_apigateway.JsonSchema(
                                type=aws_apigateway.JsonSchemaType.STRING,
                            ),
                            "date": aws_apigateway.JsonSchema(
                                type=aws_apigateway.JsonSchemaType.STRING,
                                min_length=1,
                                format="date",
                                pattern="^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$",
                            ),
                        },
                    )
                },
            ),
        )

        create_announcement_response_success_model = aws_apigateway.Model(
            self,
            "CreateAnnouncementResponseSuccess",
            model_name="CreateAnnouncementResponseSuccess",
            rest_api=api,
            schema=aws_apigateway.JsonSchema(
                type=aws_apigateway.JsonSchemaType.OBJECT,
                required=["id"],
                properties={
                    "id": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.STRING
                    )
                },
            ),
        )
        create_announcement_response_error_model = aws_apigateway.Model(
            self,
            "CreateAnnouncementResponseError",
            model_name="CreateAnnouncementResponseError",
            rest_api=api,
            schema=aws_apigateway.JsonSchema(
                type=aws_apigateway.JsonSchemaType.OBJECT,
                required=["error"],
                properties={
                    "error": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.STRING
                    )
                },
            ),
        )

        create_announcement_method = resource.add_method(
            "POST",
            integration=aws_apigateway.LambdaIntegration(
                create_announcement_lambda,
                proxy=True,
                integration_responses=[
                    aws_apigateway.IntegrationResponse(
                        status_code="200",
                        response_parameters={
                            "method.response.header.Access-Control-Allow-Origin": "'*'"
                        },
                    ),
                    aws_apigateway.IntegrationResponse(
                        status_code="404",
                        response_parameters={
                            "method.response.header.Access-Control-Allow-Origin": "'*'"
                        },
                    ),
                ],
                passthrough_behavior=aws_apigateway.PassthroughBehavior.NEVER,
            ),
            request_validator=create_announcement_request_validator,
            request_models={"application/json": create_announcement_request_model},
            method_responses=[
                aws_apigateway.MethodResponse(
                    status_code="200",
                    response_models={
                        "application/json": create_announcement_response_success_model
                    },
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True
                    },
                ),
                aws_apigateway.MethodResponse(
                    status_code="404",
                    response_models={
                        "application/json": create_announcement_response_error_model
                    },
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True
                    },
                ),
            ],
        )

        self.methods.append(create_announcement_method)
        return create_announcement_method

    def add_get_method(
        self,
        api: aws_apigateway.RestApi,
        resource: aws_apigateway.Resource,
        table: aws_dynamodb.Table,
    ):
        list_announcements_lambda = create_function(
            stack=self,
            id="ListAnnouncementLambda",
            settings={
                "handler": "list_announcements.main",
                "runtime": aws_lambda.Runtime.PYTHON_3_8,
                "timeout": core.Duration.minutes(5),
                "retry_attempts": 0,
            },
        )
        table.grant_read_data(list_announcements_lambda)
        list_announcements_lambda.add_environment(
            "TABLE_NAME",
            table.table_name,
        )

        list_announcements_method = resource.add_method(
            "GET",
            integration=aws_apigateway.LambdaIntegration(
                list_announcements_lambda,
                proxy=True,
                integration_responses=[
                    aws_apigateway.IntegrationResponse(
                        status_code="200",
                    ),
                    aws_apigateway.IntegrationResponse(
                        status_code="404",
                    ),
                ],
            ),
        )
        self.methods.append(list_announcements_method)
        return list_announcements_method
