from pydantic import BaseModel, ConfigDict

from .photo import Photo


class RecipeCategory(BaseModel):
    uuid: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class Recipe(BaseModel):
    uuid: str
    name: str
    description: str
    photo: Photo | None
    categories: list[RecipeCategory]

    model_config = ConfigDict(from_attributes=True)
