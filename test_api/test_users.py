import pytest

from fastapi.testclient import TestClient


from app import schema as s
from config import config


CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_me(client: TestClient, headers: dict[str, str], test_data: s.TestData):
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 200
    user = s.User.model_validate(response.json())
    assert user.username == test_data.test_users[0].username


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_update_user_info(client: TestClient, headers: dict[str, str]):
    new_alias = "new_alias"
    new_language = "en"
    new_wrong_language = "fr"

    response = client.get("/api/users/me", headers=headers)
    user = s.User.model_validate(response.json())

    response = client.patch("/api/users/me", headers=headers, json={"alias": new_alias})
    assert response.status_code == 200
    user = s.User.model_validate(response.json())
    assert user.alias == new_alias

    response = client.patch("/api/users/me", headers=headers, json={"language": new_language})
    assert response.status_code == 200
    user = s.User.model_validate(response.json())
    assert user.language == new_language

    response = client.patch("/api/users/me", headers=headers, json={"language": new_wrong_language})
    assert response.status_code == 422


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_delete_user(client: TestClient, headers: dict[str, str]):
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 200

    response = client.delete("/api/users/me", headers=headers)
    assert response.status_code == 204

    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 404
