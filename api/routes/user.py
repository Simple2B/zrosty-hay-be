from datetime import datetime
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


@user_router.patch("/me", status_code=status.HTTP_200_OK, response_model=s.User)
def update_user_username(
    user_update: s.UserUpdate,
    current_user: m.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Updates the current user's info"""
    update_data = user_update.dict(exclude_none=True)
    for key, value in update_data.items():
        setattr(current_user, key, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    log(log.INFO, f"User {current_user.username} was updated with language {current_user.language}")
    return current_user


@user_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    current_user: m.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Deletes the current user"""

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    current_user.is_deleted = True

    current_user.email = f"{current_user.email}_{timestamp}_deleted"
    current_user.username = f"{current_user.username}_{timestamp}_deleted"
    log(log.INFO, f"User {current_user.username} deleted his account")
    db.commit()
    return None
