from flask.testing import FlaskClient
from faker import Faker

from app import models as m, db


faker = Faker()


def test_CRU(login_client: FlaskClient):
    form_data = dict(name="Need sun", svg_icon="<path fill='red'>")

    res = login_client.post("/planting-step-types/create", data=form_data, follow_redirects=True)
    assert res.status_code == 200
    assert form_data["name"].encode("utf-8") in res.data
    step_type = db.session.get(m.PlantingStepType, 1)
    assert step_type
    assert step_type.name == form_data["name"]
    assert step_type.color == "red"

    form_data["name"] = "new name"
    form_data["color"] = "blue"
    res = login_client.post(f"/planting-step-types/{step_type.uuid}/edit", data=form_data, follow_redirects=True)
    assert res.status_code == 200
    assert form_data["name"].encode("utf-8") in res.data
