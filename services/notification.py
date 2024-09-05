from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from schemas import MessageSchema
from utils.authorization import is_authenticated
from utils.notification import send_message_to_sqs


class NotificationView(MethodView):
    @is_authenticated
    def post(self):
        try:
            payload = MessageSchema().load(request.json)
        except ValidationError as e:
            return e.messages, 400

        send_message_to_sqs(payload["subject"], payload["message"])

        return "", 200
