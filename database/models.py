from datetime import datetime
from typing import Optional

import bcrypt
import boto3
import jwt
from sqlalchemy.orm import Mapped, mapped_column

from database.config import db
from settings import SECRET_JWT, ENVIRONMENT, SMS_SNS_TOPIC_ARN, EMAIL_SNS_TOPIC_ARN


class PasswordMixin:
    password: Mapped[str] = mapped_column()

    def check_password(self, password: str) -> bool:
        password_bytes = password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, self.password.encode('utf-8'))


class User(PasswordMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()
    country_code: Mapped[Optional[str]] = mapped_column()
    phone_number: Mapped[Optional[str]] = mapped_column()
    created_at: Mapped[int] = mapped_column(default=datetime.now())
    opt_in_email: Mapped[bool] = mapped_column()
    opt_in_phone: Mapped[bool] = mapped_column()

    def update_subscription_to_sns(self):
        if ENVIRONMENT != "test":
            client = boto3.client('sns')

            if self.opt_in_email:
                client.subscribe(
                    TopicArn=EMAIL_SNS_TOPIC_ARN,
                    Protocol='email',
                    Endpoint=self.email
                )

            if self.opt_in_phone and (self.phone_number is not None) and (self.phone_number != ""):
                client.subscribe(
                    TopicArn=SMS_SNS_TOPIC_ARN,
                    Protocol='sms',
                    Endpoint=self.phone_number
                )


class ServiceUser(PasswordMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()

    def issue_token(self):
        return jwt.encode({"id": self.id}, SECRET_JWT, algorithm="HS256")
