from flask import request
from flask.views import MethodView
from marshmallow import ValidationError
from sqlalchemy import select

from database.config import db
from database.models import ServiceUser
from schemas import LoginSchema


class LoginView(MethodView):
    def post(self):
        try:
            payload = LoginSchema().load(request.json)
        except ValidationError as e:
            return e.messages, 400

        stmt = select(ServiceUser).where(ServiceUser.username == payload["username"])

        user = db.session.execute(stmt).first()

        if user is None:
            return {
                "error": "Invalid credentials"
            }, 403

        user = user[0]

        if user.check_password(payload["password"]):
            return {
                "token": user.issue_token()
            }, 200

        return {
            "error": "Invalid credentials"
        }, 403
