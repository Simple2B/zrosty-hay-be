import pytest

import sqlalchemy as sa
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app import schema as s
from app import models as m
from config import config

CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enable")
def test_get_recipe_detail(db: Session, client: TestClient):
    recipe = db.scalar(sa.select(m.Recipe))
    assert recipe
    res = client.get(f"/api/recipes/{recipe.uuid}")
    assert res.status_code == 200
    assert res.json()
    recipe_data = s.RecipeDetail.model_validate(res.json())
    assert recipe_data


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enable")
def test_get_recipe_photos(db: Session, client: TestClient):
    recipe = db.scalar(sa.select(m.Recipe))
    assert recipe
    res = client.get(f"/api/recipes/{recipe.uuid}/photos")
    assert res.status_code == 200
    assert res.json()
    photo = s.Photo.model_validate(res.json()[0])
    assert photo
