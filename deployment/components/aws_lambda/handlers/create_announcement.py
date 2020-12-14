import os
import boto3
from botocore.exceptions import ValidationError, ClientError
import uuid
from logging import getLogger


ANNOUNCEMENT_TABLE_NAME = os.environ.get("TABLE_NAME", "Announcements")

logger = getLogger(__file__)
logger.setLevel("DEBUG")


def main(event, context):
    logger.debug("Recived event: %s", event)
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(ANNOUNCEMENT_TABLE_NAME)
    item_payload = event["Item"]
    item_id = str(uuid.uuid4())
    logger.info("Received item: %s", item_payload)
    try:
        table.put_item(
            Item={
                **item_payload,
                "id": item_id,
            }
        )
    except ClientError as error:
        return {"statusCode": 404, "error": str(error.response)}

    return {"id": item_id}
