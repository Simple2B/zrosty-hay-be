import io

from flask.testing import FlaskClient
from app import models as m, db


def test_illness_crud(login_client: FlaskClient):
    # create, read
    # with open() as file:
    illness_data = dict(
        name="test_illness",
        reason="test_reason",
        symptoms="test_symptoms",
        treatment="test_treatment",
        photos=[(io.BytesIO(b"photos"), "test.jpg")],
    )
    response = login_client.post("/illness/create", data=illness_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Illness added!" in response.data
    illness: m.Illness = db.session.scalars(m.Illness.select()).first()
    assert illness

    # update
    illness_data["photos"] = []
    response = login_client.get(f"/illness/{illness.uuid}/edit", data=illness_data, follow_redirects=True)
    assert response.status_code == 200
    assert illness.name.encode("utf-8") in response.data
    NEW_NAME = "new name"
    illness_data["name"] = NEW_NAME
    illness_data["photos"] = []
    response = login_client.post(f"/illness/{illness.uuid}/edit", data=illness_data, follow_redirects=True)
    assert response.status_code == 200
    assert NEW_NAME.encode("utf-8") in response.data
    db.session.refresh(illness)
    assert illness.name == NEW_NAME

    # delete
    response = login_client.get(
        f"/illness/delete/{illness.id}",
    )
    assert response.status_code == 200
    assert b"Are you sure you want to" in response.data
    response = login_client.delete(
        f"/illness/delete/{illness.id}",
    )
    assert response.status_code == 200
    assert b"success" in response.data
    response = login_client.delete(
        f"/illness/delete/{illness.id}",
    )
    assert response.status_code == 404
