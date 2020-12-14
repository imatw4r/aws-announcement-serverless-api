import os
import boto3
from botocore.exceptions import ValidationError, ClientError
from logging import getLogger


ANNOUNCEMENT_TABLE_NAME = os.environ.get("TABLE_NAME", "Announcements")

logger = getLogger(__file__)
logger.setLevel("DEBUG")


def main(event, context):
    logger.debug("Recived event: %s", event)
    return event