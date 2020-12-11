import os
import boto3
import uuid
from logging import getLogger


ANNOUNCEMENT_TABLE_NAME = os.environ.get("ANNOUNCEMENT_TABLE_NAME", "Announcements")

logger = getLogger(__file__)
logger.setLevel("DEBUG")


def main(event, context):
    logger.debug("Recived event: %s", event)
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(ANNOUNCEMENT_TABLE_NAME)
    item_payload = event["Item"]
    item_id = str(uuid.uuid4())
    logger.info("Received item:", item)
    table.put_item(
        Item={
            **item_payload,
            "id": item_id,
        }
    )
    return {"id": item_id}
