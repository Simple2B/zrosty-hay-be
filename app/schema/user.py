from typing import Literal, Optional
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
    language: str = "ua"

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserUpdate(BaseModel):
    alias: Optional[str] = None
    language: Optional[Literal["ua", "en"]] = None
