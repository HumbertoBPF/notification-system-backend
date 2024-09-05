from flask import Flask

from database.config import db
from services.notification import NotificationView
from services.service_users import LoginView
from services.users import SignupView
from settings import ENVIRONMENT


def create_app():
    app = Flask(__name__)

    uri = "sqlite+pysqlite:///:memory:" if ENVIRONMENT == "test" else "sqlite+pysqlite:///notificationSystem.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.add_url_rule("/login", view_func=LoginView.as_view("login"))
    app.add_url_rule("/signup", view_func=SignupView.as_view("signup"))

    app.add_url_rule(
        "/send-notification",
        view_func=NotificationView.as_view("send-notification")
    )

    return app
