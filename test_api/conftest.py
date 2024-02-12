from typing import Generator
import pytest
from dotenv import load_dotenv

load_dotenv("test_api/test.env")

# ruff: noqa: F401 E402
from fastapi.testclient import TestClient
from sqlalchemy import orm

from app import schema as s
from .fake_data import init_fake_data

from api import app


@pytest.fixture
def db(test_data: s.TestData) -> Generator[orm.Session, None, None]:
    from app.database import db, get_db

    with db.Session() as session:
        db.Model.metadata.drop_all(bind=session.bind)
        db.Model.metadata.create_all(bind=session.bind)
        init_fake_data(session=session, fake_data=test_data)

        def override_get_db() -> Generator:
            yield session

        app.dependency_overrides[get_db] = override_get_db
        yield session
        # clean up
        db.Model.metadata.drop_all(bind=session.bind)


@pytest.fixture
def client(db) -> Generator[TestClient, None, None]:
    """Returns a non-authorized test client for the API"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_data() -> Generator[s.TestData, None, None]:
    """Returns a TestData object"""
    with open("test_data.json", "r") as f:
        yield s.TestData.model_validate_json(f.read())


@pytest.fixture
def headers(
    client: TestClient,
    test_data: s.TestData,
) -> Generator[dict[str, str], None, None]:
    """Returns an authorized test client for the API"""
    user = test_data.test_users[0]
    response = client.post(
        "/api/auth/login",
        data={
            "username": user.username,
            "password": user.password,
        },
    )
    assert response.status_code == 200
    token = s.Token.model_validate(response.json())

    yield dict(Authorization=f"Bearer {token.access_token}")
