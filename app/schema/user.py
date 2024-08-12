from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    id: int
    username: str
    email: str
    activated: bool = True
    avatar_url: str
    language: str = "ua"

    model_config = ConfigDict(
        from_attributes=True,
    )


class LanguageUpdate(BaseModel):
    language: str


class UsernameUpdate(BaseModel):
    username: str
