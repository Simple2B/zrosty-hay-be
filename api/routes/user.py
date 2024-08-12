from fastapi import Depends, APIRouter, status

from sqlalchemy.orm import Session

from app.database import get_db
import app.models as m
import app.schema as s
from app.logger import log

from api.dependency import get_current_user


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/me", status_code=status.HTTP_200_OK, response_model=s.User)
def get_current_user_profile(
    current_user: m.User = Depends(get_current_user),
):
    """Returns the current user profile"""

    log(log.INFO, f"User {current_user.username} requested his profile")
    return current_user


@user_router.patch("/me/language", status_code=status.HTTP_200_OK, response_model=s.User)
def update_user_language(
    language_update: s.LanguageUpdate,
    current_user: m.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Updates the current user's language"""
    if current_user.language != language_update.language:
        current_user.language = language_update.language

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    log(log.INFO, f"User {current_user.username} updated his language to {current_user.language}")
    return current_user


@user_router.patch("/me/username", status_code=status.HTTP_200_OK, response_model=s.User)
def update_user_username(
    username_update: s.UsernameUpdate,
    current_user: m.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Updates the current user's username"""
    if current_user.username != username_update.username:
        current_user.username = username_update.username

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    log(log.INFO, f"User {current_user.username} updated his username to {current_user.username}")
    return current_user


@user_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    current_user: m.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Deletes the current user"""

    if current_user.is_deleted:
        return None

    current_user.is_deleted = True

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    log(log.INFO, f"User {current_user.username} deleted his account")
    return None
