import sqlalchemy as sa

from flask.testing import FlaskClient
from faker import Faker

from .db import FakeData
from app import models as m, db


faker = Faker()


def test_plant_programs(login_client: FlaskClient, add_fake_data: FakeData):
    plant: m.PlantVariety = add_fake_data.plant_varieties[0]
    planting_step_types = add_fake_data.planting_step_types

    step_type_count = len(planting_step_types)

    form_data = {
        "planting_time": 1,
        "harvest_time": 10,
        "step_type_id": [step_type.id for step_type in planting_step_types],
        "day": [faker.random_int(min=1, max=10) for _ in range(step_type_count)],
        "instruction": [faker.paragraph(nb_sentences=5) for _ in range(step_type_count)],
    }

    res = login_client.post(f"/plant-variety/{plant.uuid}/programs/add", data=form_data, follow_redirects=True)
    assert res
    assert res.status_code == 200
    program = db.session.scalar(sa.select(m.PlantingProgram))
    assert program
    res = login_client.get(f"/planting-programs/{program.uuid}/edit")
    assert res
    assert res.status_code == 200
    assert b"Edit" in res.data
    form_data["uuid"] = [step.uuid for step in program.steps]
    form_data["instruction"] = [faker.paragraph(nb_sentences=5) for _ in range(step_type_count)]
    res = login_client.post(f"/planting-programs/{program.uuid}/edit", data=form_data, follow_redirects=True)
    assert res
    assert res.status_code == 200

    # delete program step
    step = program.steps[0]
    res = login_client.post(f"/planting-programs/{step.uuid}/delete-step", follow_redirects=True)
    assert res
    assert res.status_code == 200
    db.session.refresh(step)
    assert step.is_deleted
