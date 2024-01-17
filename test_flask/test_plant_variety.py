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
    assert b'<form action="/plant-variety/add" method="POST">' in res.data
    pest_names = faker.random_choices(
        elements=db.session.scalars(sa.Select(m.Pest.name)).all(), length=3
    )
    illness_names = faker.random_choices(
        elements=db.session.scalars(sa.Select(m.Illness.name)).all(), length=3
    )
    plant_variety_data = dict(
        plant_family_id=plant_family.id,
        name="test plant family",
        features="test plant family features",
        general_info="test plant family general info",
        temperature_info="test plant family temperature info",
        watering_info="test plant family watering info",
        planting_min_temperature=10.0,
        planting_max_temperature=20.0,
        is_moisture_loving=True,
        is_sun_loving=True,
        ground_ph=6.0,
        ground_type="test plant family ground type",
        can_plant_indoors=True,
        pests=pest_names,
        illnesses=illness_names,
    )
    res = login_client.post(
        "/plant-variety/add", data=plant_variety_data, follow_redirects=True
    )
    assert res.status_code == 200
    assert b"test plant family" in res.data
    plant_variety = db.session.get(m.PlantVariety, len(plant_varieties) + 1)
    assert plant_variety
    assert plant_variety.name == plant_variety_data["name"]
    assert plant_variety.family == plant_family
    assert [pest.name for pest in plant_variety.pests].sort() == pest_names.sort()

    # update
    res = login_client.get(f"/plant-variety/{plant_variety.uuid}/edit")
    assert res.status_code == 200
    assert (
        f'<form action="/plant-variety/{plant_variety.uuid}/edit" method="POST">'.encode(
            "utf-8"
        )
        in res.data
    )
    assert plant_variety.name.encode("utf-8") in res.data
    illness_names = faker.random_choices(
        elements=db.session.scalars(sa.Select(m.Illness.name)).all(), length=3
    )
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
    assert [
        illness.name for illness in plant_variety.illnesses
    ].sort() == illness_names.sort()
