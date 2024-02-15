import pytest

import sqlalchemy as sa
from fastapi.testclient import TestClient
from app import schema as s
from app import models as m
from config import config

CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_plant_route(db, client: TestClient):
    res = client.get("/api/plants")

    assert res.status_code == 200
    items = res.json()["items"]
    assert items
    plant = s.Plant.model_validate(items[0])
    assert plant

    res = client.get(f"/api/plants/{plant.uuid}")
    assert res.status_code == 200
    plant_detail = s.PlantDetail.model_validate(res.json())
    assert plant_detail

    cur_plant: m.PlantVariety = db.scalar(sa.select(m.PlantVariety).where(m.PlantVariety.uuid == plant.uuid))
    cur_plant._photos = [m.Photo(url_path="http://example.com", original_name="test.jpg")]
    db.commit()

    res = client.get(f"/api/plants/{plant.uuid}/photos")
    assert res.status_code == 200
    assert res.json()

    day = 1
    program = m.PlantingProgram(planting_time=1, harvest_time=1)
    program.steps.append(m.PlantingStep(day=day, instruction="test", step_type_id=1))
    cur_plant.programs.append(program)
    db.commit()
    res = client.get(f"/api/plants/{plant.uuid}/steps")
    assert res.status_code == 200
    assert res.json()[0]["day"] == day

    res = client.get(f"/api/plants/{plant.uuid}/steps/{day}")
    assert res.status_code == 200
    assert res.json()

    categories = db.scalars(sa.select(m.PlantCategory)).all()
    cur_plant.family.categories = categories  # type:ignore
    db.commit()
    res = client.get(f"/api/plants/?category_uuids={categories[0].uuid}")
    assert res.status_code == 200
    plant = s.Plant.model_validate(items[0])
    assert plant


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enable")
def test_get_plant_recipes(db, client: TestClient):
    plant: m.PlantVariety = db.scalar(sa.select(m.PlantVariety))
    res = client.get(f"/api/plants/{plant.uuid}/recipes")
    assert res.status_code == 200
    assert res.json()
    recipe = s.Recipe.model_validate(res.json()["items"][0])
    assert recipe


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_categories(db, client: TestClient):
    res = client.get("/api/plants/categories")

    assert res.status_code == 200
    plant = s.PlantCategory.model_validate(res.json()[0])
    assert plant
