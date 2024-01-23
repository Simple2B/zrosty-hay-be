import pytest
from fastapi.testclient import TestClient
from app import schema as s
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
