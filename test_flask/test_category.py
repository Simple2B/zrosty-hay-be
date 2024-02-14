from flask.testing import FlaskClient


from app import models as m, db


def test_CRU(login_client: FlaskClient):
    form_data = dict(name="Need sun")

    res = login_client.post("/categories/create", data=form_data, follow_redirects=True)
    assert res.status_code == 200
    assert form_data["name"].encode("utf-8") in res.data
    category = db.session.get(m.Category, 1)
    assert category
    assert category.name == form_data["name"]

    form_data["name"] = "new name"
    res = login_client.post(f"/categories/{category.uuid}/edit", data=form_data, follow_redirects=True)
    assert res.status_code == 200
    assert form_data["name"].encode("utf-8") in res.data
