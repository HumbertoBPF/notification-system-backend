from datetime import datetime

import pytest

from app_factory import create_app
from database.config import db
from database.models import ServiceUser, User
from utils.hashing import hash_password


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield


@pytest.fixture
def service_user(app, faker):
    with app.app_context():
        user = ServiceUser(
            username=faker.user_name(),
            password=hash_password("str0ng-P@ssw0rd")
        )
        db.session.add(user)
        db.session.commit()
        db.session.close()
    return user


@pytest.fixture
def user(app, faker):
    with app.app_context():
        user = User(
            email=faker.email(),
            country_code="en-us",
            phone_number="+55 16 91234 5678",
            created_at=datetime.now(),
            password=hash_password("str0ng-P@ssw0rd"),
            opt_in_email=True,
            opt_in_phone=True
        )
        db.session.add(user)
        db.session.commit()
        db.session.close()
    return user
