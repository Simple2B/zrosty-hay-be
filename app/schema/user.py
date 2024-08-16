from typing import Optional
from app.constants import UserPreferredLanguage
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    id: int
    username: str
    alias: str
    email: str
    activated: bool = True
    avatar_url: str
    language: UserPreferredLanguage

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserUpdate(BaseModel):
    alias: Optional[str] = None
    language: Optional[UserPreferredLanguage] = None
