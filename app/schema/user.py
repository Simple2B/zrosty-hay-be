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

    model_config = ConfigDict(
        from_attributes=True,
    )
