from typing import TypedDict

from aws_cdk import aws_dynamodb
from aws_cdk import core


class DynamoDBSettings(TypedDict):
    table_name: str
    read_capacity: int
    write_capacity: int


def create_table(stack: core.Stack, settings: DynamoDBSettings, **kwargs):
    return aws_dynamodb.Table(
        stack,
        "Table",
        table_name=settings.get("table_name", "Announcements"),
        partition_key=aws_dynamodb.Attribute(
            name="id", type=aws_dynamodb.AttributeType.STRING
        ),
        sort_key=aws_dynamodb.Attribute(
            name="date", type=aws_dynamodb.AttributeType.STRING
        ),
        read_capacity=settings.get("read_capacity", 5),
        write_capacity=settings.get("write_capacity", 4),
        removal_policy=core.RemovalPolicy.DESTROY,
        **kwargs,
    )

    core.CfnOutput(self, "AnnouncementTableName", value=self.table.table_name)