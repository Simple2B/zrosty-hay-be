from flask import current_app as app
from flask.testing import FlaskClient, FlaskCliRunner
from click.testing import Result
from app import models as m, db
from test_flask.utils import login

TEST_NAME = "test_pets"


def test_pest_crud(login_client: FlaskClient):
    pest_data = dict(
        name=TEST_NAME,
        symptoms="test_symptoms",
        treatment="test_treatment",
    )
    response = login_client.post(
        "/pest/create",
        data=pest_data,
    )
    assert response.status_code == 302
    pest: m.Pest = db.session.scalars(m.Pest.select()).first()
    assert pest

    # test updated
    NEW_NAME = "some name"
    pest_data["pest_id"] = str(pest.id)
    pest_data["name"] = NEW_NAME
    response = login_client.post("/pest/save", data=pest_data, follow_redirects=True)
    assert response.status_code == 200
    assert NEW_NAME.encode("utf-8") in response.data

    pest_data["pest_id"] = "100"
    response = login_client.post("/pest/save", data=pest_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Cannot save pest data" in response.data

    # test delete
    response = login_client.delete(
        f"/pest/delete/{pest.id}", data=pest_data, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"ok" in response.data
    response = login_client.delete(
        f"/pest/delete/{pest.id}", data=pest_data, follow_redirects=True
    )
    assert response.status_code == 404
    assert b"no pest" in response.data


def test_populate_db(runner: FlaskCliRunner):
    TEST_COUNT = 56
    count_before = db.session.query(m.User).count()
    res: Result = runner.invoke(args=["db-populate", "--count", f"{TEST_COUNT}"])
    assert f"populated by {TEST_COUNT}" in res.stdout
    assert (db.session.query(m.User).count() - count_before) == TEST_COUNT


def test_delete_user(populate: FlaskClient):
    login(populate)
    uc = db.session.query(m.User).count()
    response = populate.delete("/user/delete/1")
    assert db.session.query(m.User).count() < uc
    assert response.status_code == 200
