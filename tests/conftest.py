import pytest
from app import app as flask_app


@pytest.fixture
def app():
    flask_app.config.update({"TESTING": True, "SECRET-KEY": "test-secret"})
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def fake_user(app):
    user_pas = "test", "testing"
    return app.test_client(user_pas)
