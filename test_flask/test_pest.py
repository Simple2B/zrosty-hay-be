from flask import current_app as app
from flask.testing import FlaskClient, FlaskCliRunner
from click.testing import Result
from app import models as m, db
from test_flask.utils import login


def test_pest_crud(login_client: FlaskClient):
    data = dict(
        name="test_pest",
        symptoms="test_symptoms",
        treatment="test_treatment",
    )
    response = login_client.post(
        "/pest/create",
        data=data,
    )
    assert response.status_code == 201
    pest_rows_objs = db.session.execute(m.Pest.select()).all()
    assert len(pest_rows_objs) > 0


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
