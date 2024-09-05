import pytest

from database.config import db

url = "/login"


@pytest.mark.usefixtures("app_ctx")
def test_login_requires_username(client, service_user):
    db.session.add(service_user)

    response = client.post(url, json={
        "password": "str0ng-P@ssw0rd"
    })

    assert response.status_code == 400
    assert response.json["username"] == ["Missing data for required field."]

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_login_requires_password(client, service_user):
    db.session.add(service_user)

    response = client.post(url, json={
        "username": service_user.username,
    })

    assert response.status_code == 400
    assert response.json["password"] == ["Missing data for required field."]

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_login_invalid_username(client, service_user):
    db.session.add(service_user)

    response = client.post(url, json={
        "username": f"a{service_user.username}",
        "password": "str0ng-P@ssw0rd"
    })

    assert response.status_code == 403
    assert response.json["error"] == "Invalid credentials"

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_login_invalid_password(client, service_user):
    db.session.add(service_user)

    response = client.post(url, json={
        "username": service_user.username,
        "password": "Str0ng-P@ssw0rd"
    })

    assert response.status_code == 403
    assert response.json["error"] == "Invalid credentials"

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_login(client, service_user):
    db.session.add(service_user)

    response = client.post(url, json={
        "username": service_user.username,
        "password": "str0ng-P@ssw0rd"
    })

    assert response.status_code == 200
    assert "token" in response.json

    db.session.close()
