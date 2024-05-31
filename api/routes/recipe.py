from fastapi import APIRouter, Depends, status

import app.models as m
import app.schema as s
from app.logger import log
from api.dependency import get_recipe


router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get(
    "/{uuid}",
    status_code=status.HTTP_200_OK,
    response_model=s.RecipeDetail,
    responses={404: {"model": s.ApiError404}},
)
def get_recipe_detail(uuid: str, recipe: m.Recipe = Depends(get_recipe)):
    """Returns the recipe detail"""
    return recipe


@router.get(
    "/{uuid}/photos",
    status_code=status.HTTP_200_OK,
    response_model=list[s.Photo],
    responses={404: {"model": s.ApiError404}},
)
def get_plant_photos(uuid: str, recipe: m.Recipe = Depends(get_recipe)):
    """Returns the plant photos"""
    log(log.INFO, "Get plant photos uuid[%s]", uuid)

    return recipe.photos
