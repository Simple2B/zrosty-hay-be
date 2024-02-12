import pytest

from fastapi.testclient import TestClient
from app import schema as s
from config import config

CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_step_types(db, client: TestClient):
    res = client.get("/api/planting-step-types")
    assert res
    assert res.status_code == 200
    assert res.json()
    assert s.PlantingStepType.model_validate(res.json()[0])
