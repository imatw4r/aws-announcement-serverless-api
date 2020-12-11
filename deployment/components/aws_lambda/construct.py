import os
from typing import Dict, List, Optional, TypedDict

from aws_cdk import aws_lambda
from aws_cdk import aws_s3
from aws_cdk import core

HANDLERS_DIRECTORY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "handlers"
)


class LambdaConfig(TypedDict):
    handler: str
    runtime: aws_lambda.Runtime
    environment: Optional[Dict[str, str]] = {}
    timeout: core.Duration.minutes
    retry_attempts: int


class LambdaConstructProps(TypedDict):
    lambda_config: LambdaConfig


class CreateAnnouncementLambda(core.Construct):
    def __init__(self, scope, id, props: LambdaConstructProps):
        super().__init__(scope, id)
        self.props = props
        self.function = aws_lambda.Function(
            self,
            id,
            **props["lambda_config"],
            function_name=core.PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset(HANDLERS_DIRECTORY),
            tracing=aws_lambda.Tracing.ACTIVE
        )
