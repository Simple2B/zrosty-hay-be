import io

from flask.testing import FlaskClient
import sqlalchemy as sa
from faker import Faker

from .db import FakeData
from app import models as m, db


faker = Faker()


def test_plant_varieties_cru(login_client: FlaskClient, add_fake_data: FakeData):
    """CRU (Create, Read, Update) tests for plant variety"""
    # read
    plant_varieties = add_fake_data.plant_varieties
    plant_family = add_fake_data.plant_families[-1]
    res = login_client.get("/plant-variety/")
    assert res.status_code == 200
    assert plant_varieties[-1].name.encode("utf-8") in res.data

    # create
    res = login_client.get("/plant-variety/add")
    assert res.status_code == 200
    assert b'action="/plant-variety/add" method="POST"' in res.data
    pest_names = faker.random_choices(elements=db.session.scalars(sa.select(m.Pest.name)).all(), length=3)
    illness_names = faker.random_choices(elements=db.session.scalars(sa.select(m.Illness.name)).all(), length=3)
    plant_variety_data = dict(
        plant_family_id=plant_family.id,
        name="test plant family",
        features="test plant family features",
        general_info="test plant family general info",
        temperature_info="test plant family temperature info",
        watering_info="test plant family watering info",
        planting_min_temperature=10.0,
        planting_max_temperature=20.0,
        min_size=1,
        max_size=10,
        humidity_percentage=30,
        water_volume=40,
        care_type=m.CareType.hard.value,
        is_moisture_loving=True,
        is_sun_loving=True,
        ground_ph=6.0,
        ground_type="test plant family ground type",
        can_plant_indoors=True,
        pests=pest_names,
        illnesses=illness_names,
        photos=[(io.BytesIO(b"photos"), "test.jpg")],
    )
    res = login_client.post("/plant-variety/add", data=plant_variety_data, follow_redirects=True)
    assert res.status_code == 200
    assert b"test plant family" in res.data
    plant_variety = db.session.get(m.PlantVariety, len(plant_varieties) + 1)
    assert plant_variety
    assert plant_variety.photos
    assert plant_variety.name == plant_variety_data["name"]
    assert plant_variety.family == plant_family
    assert [pest.name for pest in plant_variety.pests].sort() == pest_names.sort()

    # update
    plant_variety_data["photos"] = []
    res = login_client.get(f"/plant-variety/{plant_variety.uuid}/edit")
    assert res.status_code == 200
    assert f'action="/plant-variety/{plant_variety.uuid}/edit" method="POST'.encode("utf-8") in res.data
    assert plant_variety.name.encode("utf-8") in res.data
    illness_names = faker.random_choices(elements=db.session.scalars(sa.select(m.Illness.name)).all(), length=3)
    NEW_NAME = "updated plant variety name"
    del plant_variety_data["plant_family_id"]
    plant_variety_data["name"] = NEW_NAME
    plant_variety_data["illnesses"] = illness_names
    res = login_client.post(
        f"/plant-variety/{plant_variety.uuid}/edit",
        data=plant_variety_data,
        follow_redirects=True,
    )
    assert res.status_code == 200
    assert NEW_NAME.encode("utf-8") in res.data
    db.session.refresh(plant_variety)
    assert plant_variety.name == NEW_NAME
    assert [illness.name for illness in plant_variety.illnesses].sort() == illness_names.sort()


def test_create_and_get_plant_variety_program(login_client: FlaskClient, add_fake_data: FakeData):
    plant_variety = add_fake_data.plant_varieties[0]
    res = login_client.get(f"/plant-variety/{plant_variety.uuid}/programs")

    assert res.status_code == 200
    assert b"Add program" in res.data

    res = login_client.get(f"/plant-variety/{plant_variety.uuid}/programs/add")
    assert res.status_code == 200
    assert f"{plant_variety.uuid}".encode("utf-8") in res.data
    step_type = add_fake_data.planting_step_types[0]

    form_data = dict(
        planting_time=10, harvest_time=10, day=["1"], instruction=["some text"], step_type_id=[step_type.id]
    )

    res = login_client.post(f"/plant-variety/{plant_variety.uuid}/programs/add", data=form_data, follow_redirects=True)
    assert res.status_code == 200
    program = db.session.get(m.PlantingProgram, 1)
    assert program
    assert program.planting_time == form_data["planting_time"]
    assert program.harvest_time == form_data["harvest_time"]
    assert program.steps
    assert program.steps[0].step_type_id == step_type.id
