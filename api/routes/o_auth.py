import sqlalchemy as sa

from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests


from config import config
import app.models as m
import app.schema as s
from app.logger import log

from api import controllers as api_c
from api.dependency import get_db
from api.oauth2 import create_access_token

ISSUER_WHITELIST = ["accounts.google.com", "https://accounts.google.com"]

router = APIRouter(prefix="/o_auth", tags=["O-Auth"])

CFG = config()


@router.post("/google_validate", status_code=status.HTTP_200_OK, response_model=s.Token)
def validate_google_token(auth_data: s.GoogleAuthTokenIn, db: Session = Depends(get_db)):
    """Validates google auth token and returns a JWT token"""
    log(log.INFO, "Validating google token")

    try:
        id_info_res = id_token.verify_oauth2_token(
            auth_data.id_token,
            requests.Request(),
            CFG.GOOGLE_CLIENT_ID,
        )

        id_info = s.GoogleTokenVerification.model_validate(id_info_res)

        if id_info.iss not in ISSUER_WHITELIST:
            raise ValueError("Wrong issuer.")

        user = db.scalar(
            sa.select(m.User).where(
                m.User.email == id_info.email,
            )
        )

        if not user:
            log(log.INFO, "[Google Auth] User [%s] not found. Creating a guest user", id_info.email)
            user = api_c.create_guest_user(db, id_info.email, id_info.name, id_info.picture)
        return s.Token(access_token=create_access_token(user.id))

    except HTTPException as e:
        raise e

    except ValidationError as e:
        log(log.ERROR, "Invalid GoogleTokenVerification value: %s", e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

    except ValueError as e:
        log(log.ERROR, "Invalid token: %s", e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")


@router.post("/apple_validate", status_code=status.HTTP_200_OK, response_model=s.Token)
def validate_apple_token(auth_data: s.AppleAuthTokenIn, db: Session = Depends(get_db)):
    log(log.INFO, "Validating apple token")

    decoded_token = api_c.verify_apple_token(auth_data)

    user = db.scalar(
        sa.select(m.User).where(
            m.User.email == decoded_token.email,
        )
    )

    if not user:
        log(log.INFO, "[Apple Auth] User [%s] not found. Creating a guest user", decoded_token.email)
        alias = api_c.get_apple_username(decoded_token)
        user = api_c.create_guest_user(db, decoded_token.email, alias)

    log(log.INFO, "User [%s] found. Apple Auth succeeded", decoded_token.email)
    return s.Token(access_token=create_access_token(user.id))
