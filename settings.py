import os

from dotenv import load_dotenv

load_dotenv()

SECRET_JWT = os.getenv("SECRET_JWT")
ENVIRONMENT = os.getenv("ENVIRONMENT")

EMAIL_SNS_TOPIC_ARN = os.getenv("EMAIL_SNS_TOPIC_ARN")
SMS_SNS_TOPIC_ARN = os.getenv("SMS_SNS_TOPIC_ARN")

EMAIL_SQS_QUEUE_URL = os.getenv("EMAIL_SQS_QUEUE_URL")
SMS_SQS_QUEUE_URL = os.getenv("SMS_SQS_QUEUE_URL")
