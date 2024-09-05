import json
import uuid

import boto3

from settings import ENVIRONMENT, EMAIL_SQS_QUEUE_URL, SMS_SQS_QUEUE_URL


def send_message_to_sqs(subject: str, message: str):
    if ENVIRONMENT != "test":
        client = boto3.client('sqs')

        client.send_message(
            QueueUrl=EMAIL_SQS_QUEUE_URL,
            MessageBody=json.dumps({"subject": subject, "message": message}),
            MessageGroupId="id",
            MessageDeduplicationId=str(uuid.uuid4())
        )

        client.send_message(
            QueueUrl=SMS_SQS_QUEUE_URL,
            MessageBody=json.dumps({"subject": subject, "message": message}),
            MessageGroupId="id",
            MessageDeduplicationId=str(uuid.uuid4())
        )
