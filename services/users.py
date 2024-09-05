from flask import request
from flask.views import MethodView
from marshmallow import ValidationError
from sqlalchemy import select

from database.config import db
from database.models import User
from schemas import SignupSchema
from utils.hashing import hash_password


class SignupView(MethodView):
    def post(self):
        try:
            payload = SignupSchema().load(request.json)
        except ValidationError as e:
            return e.messages, 400

        stmt = select(User).where(User.email == payload["email"])
        user = db.session.execute(stmt).first()

        if user is not None:
            return {
                "email": ["This field must be unique."]
            }, 400

        user = User(
            email=payload["email"],
            country_code=payload["country_code"],
            phone_number=payload["phone_number"],
            password=hash_password(payload["password"]),
            opt_in_email=payload["opt_in_email"],
            opt_in_phone=payload["opt_in_phone"]
        )
        db.session.add(user)
        db.session.commit()

        user.update_subscription_to_sns()

        db.session.close()

        return "", 201
