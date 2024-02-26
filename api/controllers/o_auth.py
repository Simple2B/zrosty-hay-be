import jwt

from jwt import PyJWKClient
from sqlalchemy.orm import Session
from app.constants import UserRole

from config import config
from app import schema as s
from app import models as m

CFG = config()


CFG = config()

JWKS_CLIENT = PyJWKClient(CFG.APPLE_PUBLIC_KEY_URL)


def verify_apple_token(auth_data: s.AppleAuthTokenIn) -> s.AppleTokenVerification:
    """Verifies the Apple auth token and returns the decoded token"""
    # Fetch Apple's public keys
    signing_key = JWKS_CLIENT.get_signing_key_from_jwt(auth_data.id_token)
    apple_public_key = signing_key.key

    # Verify the signature using the fetched public key
    decoded_token_raw = jwt.decode(
        auth_data.id_token,
        apple_public_key,
        issuer=CFG.APPLE_ISSUER,
        audience=CFG.MOBILE_APP_ID,
        algorithms=CFG.APPLE_DECODE_ALGORITHMS,
    )

    decoded_token = s.AppleTokenVerification.model_validate(decoded_token_raw)
    return decoded_token


def create_guest_user(
    db: Session,
    email: str,
    alias: str,
) -> m.User:
    """Creates a guest user in the database"""
    guest_user = m.User(
        email=email,
        alias=alias,
        activated=True,
        # We create a random username and password, so guest won't ba able to login with manual credentials, only with Oauth
        username=m.gen_password_reset_id(),
        password=m.gen_password_reset_id(),
        role=UserRole.user.value,
    )
    db.add(guest_user)
    db.commit()

    return guest_user


def get_apple_username(decoded_token: s.AppleTokenVerification) -> str:
    if not decoded_token.fullName:
        return decoded_token.email.split("@")[0]
    if not decoded_token.fullName.givenName and not decoded_token.fullName.familyName:
        return decoded_token.email
    return f"{decoded_token.fullName.givenName} {decoded_token.fullName.familyName}".strip()
