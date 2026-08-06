import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from app import create_app
from app.extensions import db, bcrypt
from app.models import Well, Company, Account


@pytest.fixture()
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def well(app):
    with app.app_context():
        company = Company(name="Test Co", region="Test Region")
        db.session.add(company)
        db.session.flush()

        w = Well(
            name="Test Well 1",
            type="oil",
            max_drilling_depth=1500.0,
            oil_company_id=company.id,
        )
        db.session.add(w)
        db.session.commit()
        return w.id


@pytest.fixture()
def auth_client(app, client):
    """Test client logged in as a test Account."""
    with app.app_context():
        hashed_pw = bcrypt.generate_password_hash("testpass123").decode("utf-8")
        account = Account(username="testuser", password=hashed_pw)
        db.session.add(account)
        db.session.commit()

    client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpass123"},
        follow_redirects=True,
    )
    return client