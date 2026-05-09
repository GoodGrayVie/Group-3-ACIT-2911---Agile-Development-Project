import pytest
from app import app as flask_app
from db.models import db
from db.seed import seed


@pytest.fixture
def app():
    flask_app.config.update({"TESTING": True, "SECRET-KEY": "test-secret"})
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def workout_data(app):
    # test creating workout and exersises and saving to db
    pass

@pytest.fixture
def fake_user(app):
    # make user to check user authentication
    pass
