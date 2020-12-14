import os
from typing import Dict, List, Optional, TypedDict

from aws_cdk import aws_lambda
from aws_cdk import aws_s3
from aws_cdk import core
from aws_cdk import aws_dynamodb

HANDLERS_DIRECTORY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "handlers"
)


class LambdaConfig(TypedDict):
    handler: str
    runtime: aws_lambda.Runtime
    timeout: core.Duration.minutes
    retry_attempts: int


def create_function(
    stack: core.Stack, id: str, settings: LambdaConfig, **kwargs
) -> aws_lambda.Function:
    return aws_lambda.Function(
        stack,
        id,
        **settings,
        function_name=core.PhysicalName.GENERATE_IF_NEEDED,
        code=aws_lambda.Code.from_asset(HANDLERS_DIRECTORY),
        tracing=aws_lambda.Tracing.ACTIVE,
        **kwargs
    )
