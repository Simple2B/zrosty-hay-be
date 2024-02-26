from unittest import mock
import pytest
import sqlalchemy as sa

from app.schema import GoogleTokenVerification, Token, AppleTokenVerification
from config import config
from app.models import User


MOCK_CLIENT_ID = "test_client_id"
CFG = config()


DUMMY_GOOGLE_VALIDATION = GoogleTokenVerification(
    iss="https://accounts.google.com",
    email="test@example.com",
    azp="str",
    aud="str",
    sub="str",
    email_verified=True,
    name="str",
    picture="str",
    given_name="str",
    family_name="str",
    locale="str",
    iat=1,
    exp=1,
)

DUMMY_IOS_VALIDATION = AppleTokenVerification(
    iss="https://appleid.apple.com",
    aud="str",
    exp=1,
    iat=1,
    sub="str",
    c_hash="str",
    email="",
    email_verified=True,
    auth_time=1,
    nonce_supported=True,
    fullName=None,
)


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_validate_google_token_success(monkeypatch, db, client):
    # Mock the id_token.verify_oauth2_token method
    mock_verify_oauth2_token = mock.Mock(return_value=DUMMY_GOOGLE_VALIDATION)
    monkeypatch.setattr("api.routes.o_auth.id_token.verify_oauth2_token", mock_verify_oauth2_token)

    # Create a test user in the database
    user = User(email="test@example.com", username="test", password="test")
    db.add(user)
    db.commit()

    # Make a request to the endpoint
    response = client.post("/api/o_auth/google_validate", json={"id_token": "test_token"})

    # Check the response
    assert response.status_code == 200
    token = Token.model_validate(response.json())
    assert len(token.access_token) > 0

    # Check that the mock method was called with the correct arguments
    mock_verify_oauth2_token.assert_called_once_with(
        "test_token",
        mock.ANY,  # requests.Request() is passed as the second argument
        CFG.GOOGLE_CLIENT_ID,
    )


# Create test for Google validation with guest user creation and token generation when user is not in database, but token is valid
@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_validate_google_token_guest_user_creation(monkeypatch, db, client):
    # Mock the id_token.verify_oauth2_token method
    mock_verify_oauth2_token = mock.Mock(return_value=DUMMY_GOOGLE_VALIDATION)
    monkeypatch.setattr("api.routes.o_auth.id_token.verify_oauth2_token", mock_verify_oauth2_token)

    # Send a request to the endpoint
    response = client.post("/api/o_auth/google_validate", json={"id_token": "test_token"})
    assert response.status_code == 200

    # Check that the mock method was called with the correct arguments
    mock_verify_oauth2_token.assert_called_once_with(
        "test_token",
        mock.ANY,  # requests.Request() is passed as the second argument
        CFG.GOOGLE_CLIENT_ID,
    )

    # Check that the user was created in the database
    user = db.scalar(sa.select(User).where(User.email == DUMMY_GOOGLE_VALIDATION.email))
    assert user is not None


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_validate_apple_token_success(monkeypatch, db, client):
    # Mock verify_apple_token from api/controllers/o_auth.py
    mock_verify_apple_token = mock.Mock(return_value=DUMMY_IOS_VALIDATION)
    monkeypatch.setattr("api.routes.o_auth.api_c.verify_apple_token", mock_verify_apple_token)

    res = client.post(
        "/api/o_auth/apple_validate",
        json={"id_token": ""},
    )

    assert res.status_code == 200
