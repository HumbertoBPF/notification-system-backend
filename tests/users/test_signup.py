import random

import pytest
from sqlalchemy import select

from database.config import db
from database.models import User

url = "/signup"


@pytest.mark.parametrize("missing_param", ["email", "password", "opt_in_email", "opt_in_phone"])
def test_signup_required_parameters(client, faker, missing_param):
    payload = {
        "email": faker.email(),
        "password": "Str0ng-P@ssw0rd",
        "opt_in_email": random.choice([True, False]),
        "opt_in_phone": random.choice([True, False])
    }

    del payload[missing_param]

    response = client.post(url, json=payload)

    assert response.status_code == 400
    assert response.json[missing_param] == ["Missing data for required field."]


@pytest.mark.usefixtures("app_ctx")
def test_signup_email_must_be_unique(client, user):
    db.session.add(user)

    payload = {
        "email": user.email,
        "password": "Str0ng-P@ssw0rd",
        "opt_in_email": random.choice([True, False]),
        "opt_in_phone": random.choice([True, False])
    }

    response = client.post(url, json=payload)

    assert response.status_code == 400
    assert response.json["email"] == ["This field must be unique."]


@pytest.mark.usefixtures("app_ctx")
def test_signup_defaults(client, faker):
    payload = {
        "email": faker.email(),
        "password": "Str0ng-P@ssw0rd",
        "opt_in_email": random.choice([True, False]),
        "opt_in_phone": random.choice([True, False])
    }

    response = client.post(url, json=payload)

    assert response.status_code == 201

    stmt = select(User).where(User.email == payload["email"])
    user = db.session.execute(stmt).first()[0]

    assert user.check_password(payload["password"])
    assert user.country_code == "en-us"
    assert user.phone_number is None
    assert user.opt_in_email is payload["opt_in_email"]
    assert user.opt_in_phone is payload["opt_in_phone"]


@pytest.mark.usefixtures("app_ctx")
def test_signup(client, faker):
    payload = {
        "email": faker.email(),
        "country_code": "pt-br",
        "phone_number": faker.phone_number(),
        "password": "Str0ng-P@ssw0rd",
        "opt_in_email": random.choice([True, False]),
        "opt_in_phone": random.choice([True, False])
    }

    response = client.post(url, json=payload)

    assert response.status_code == 201

    stmt = select(User).where(User.email == payload["email"])
    user = db.session.execute(stmt).first()[0]

    assert user.check_password(payload["password"])
    assert user.country_code == payload["country_code"]
    assert user.phone_number == payload["phone_number"]
    assert user.opt_in_email is payload["opt_in_email"]
    assert user.opt_in_phone is payload["opt_in_phone"]
