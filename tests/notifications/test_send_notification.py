import pytest

from database.config import db

url = "/send-notification"


@pytest.mark.usefixtures("app_ctx")
def test_send_notification_requires_authentication(client, service_user, user):
    db.session.add(service_user)
    db.session.add(user)

    response = client.post(url)

    assert response.status_code == 403
    assert response.json["error"] == "Invalid authorization header"

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_send_notification_invalid_authorization_header(client, service_user, user):
    db.session.add(service_user)
    db.session.add(user)

    response = client.post(url, headers={"Authorization": "Bearer invalid"})

    assert response.status_code == 403
    assert response.json["error"] == "Invalid authorization header"

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_send_notification_requires_subject(client, service_user, user, faker):
    db.session.add(service_user)
    db.session.add(user)

    response = client.post(
        url,
        json={
            "message": faker.text()
        },
        headers={"Authorization": f"Bearer {service_user.issue_token()}"}
    )

    assert response.status_code == 400
    assert response.json["subject"] == ["Missing data for required field."]

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_send_notification_requires_message(client, service_user, user, faker):
    db.session.add(service_user)
    db.session.add(user)

    response = client.post(
        url,
        json={
            "subject": faker.word()
        },
        headers={"Authorization": f"Bearer {service_user.issue_token()}"}
    )

    assert response.status_code == 400
    assert response.json["message"] == ["Missing data for required field."]

    db.session.close()


@pytest.mark.usefixtures("app_ctx")
def test_send_notification(client, service_user, user, faker):
    db.session.add(service_user)
    db.session.add(user)

    response = client.post(url, json={
        "subject": faker.word(),
        "message": faker.text()
    }, headers={"Authorization": f"Bearer {service_user.issue_token()}"})

    assert response.status_code == 200

    db.session.close()
