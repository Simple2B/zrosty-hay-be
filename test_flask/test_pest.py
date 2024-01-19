import io

from flask.testing import FlaskClient
from app import models as m, db
from test_flask.utils import login

TEST_NAME = "test_pets"


def test_pest_crud(login_client: FlaskClient):
    pest_data = dict(
        name=TEST_NAME,
        symptoms="test_symptoms",
        treatment="test_treatment",
        photos=[(io.BytesIO(b"photos"), "test.jpg")],
    )
    response = login_client.post(
        "/pest/create",
        data=pest_data,
    )
    assert response.status_code == 302
    pest: m.Pest = db.session.scalars(m.Pest.select()).first()
    assert pest
    assert pest.photos

    # test updated
    response = login_client.get(f"/pest/{pest.uuid}/edit", follow_redirects=True)
    assert response.status_code == 200
    assert pest.name.encode("utf-8") in response.data

    NEW_NAME = "some name"
    pest_data["name"] = NEW_NAME
    pest_data["photos"] = []
    response = login_client.post(f"/pest/{pest.uuid}/edit", data=pest_data, follow_redirects=True)
    assert response.status_code == 200
    assert NEW_NAME.encode("utf-8") in response.data

    # test delete
    response = login_client.delete(f"/pest/delete/{pest.id}", data=pest_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"ok" in response.data
    response = login_client.delete(f"/pest/delete/{pest.id}", data=pest_data, follow_redirects=True)
    assert response.status_code == 404
    assert b"no pest" in response.data


def test_delete_user(populate: FlaskClient):
    login(populate)
    uc = db.session.query(m.User).count()
    response = populate.delete("/user/delete/1")
    assert db.session.query(m.User).count() < uc
    assert response.status_code == 200
