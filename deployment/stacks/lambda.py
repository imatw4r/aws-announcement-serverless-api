from aws_cdk import core
from aws_cdk import aws_dynamodb


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
