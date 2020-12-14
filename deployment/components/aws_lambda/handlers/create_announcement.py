from typing import TypedDict
import json
import os
import boto3
from botocore.exceptions import ValidationError, ClientError
import uuid
from logging import getLogger


ANNOUNCEMENT_TABLE_NAME = os.environ.get("TABLE_NAME")

logger = getLogger(__file__)
logger.setLevel("DEBUG")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(ANNOUNCEMENT_TABLE_NAME)


class Announcement(TypedDict):
    title: str
    description: str
    date: str  # YYYY-MM-DD format


def main(event, context):
    logger.debug("Recived event: %s", event)
    body = json.loads(event["body"])
    item_payload: Announcement = body["Item"]
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
        return {
            "statusCode": 404,
            "body": json.dumps({"error": str(error.response["Error"]["Message"])}),
        }

    return {"statusCode": 200, "body": json.dumps({"id": item_id})}
