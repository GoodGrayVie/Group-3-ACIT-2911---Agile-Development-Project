import pytest
from werkzeug.security import generate_password_hash
from agent_api import create_app
from db.models import db, User


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        db.create_all()

        # Create test users needed across all tests
        users = [
            {"name": "testuser", "email": "testuser@test.com", "password": "password123"},
            {"name": "Tom",      "email": "tom@test.com",      "password": "pass1234"},
        ]
        for u in users:
            if not User.query.filter_by(name=u["name"]).first():
                db.session.add(User(
                    name=u["name"],
                    email=u["email"],
                    hashed_password=generate_password_hash(u["password"])
                ))
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()