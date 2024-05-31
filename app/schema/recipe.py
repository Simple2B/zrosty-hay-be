from pydantic import BaseModel, ConfigDict, Field

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


class RecipeIngredient(BaseModel):
    name: str
    quantity: float
    quantity_type: str = Field(alias="quantityType")
    photo: Photo | None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class RecipeAdditionalIngredient(BaseModel):
    name: str
    text_quantity: str = Field(alias="textQuantity")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class RecipeStep(BaseModel):
    step_number: int = Field(alias="stepNumber")
    instruction: str = Field(alias="instruction")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class RecipeDetail(BaseModel):
    name: str
    cooking_time: int
    ingredients: list[RecipeIngredient] = []
    additional_ingredients: list[RecipeAdditionalIngredient] = Field([], alias="additionalIngredients")
    steps: list[RecipeStep] = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
