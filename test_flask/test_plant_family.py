from flask.testing import FlaskClient
import sqlalchemy as sa
from faker import Faker

from app import models as m, db
from .db import FakeData

faker = Faker()


def test_plant_families_cru(login_client: FlaskClient, add_fake_data: FakeData):
    """CRU (Create, Read, Update) tests for plant family"""
    # read
    plant_families = add_fake_data.plant_families
    res = login_client.get("/plant-family/")
    assert res.status_code == 200
    assert plant_families[-1].name.encode("utf-8") in res.data

    # create
    res = login_client.get("/plant-family/create")
    assert res.status_code == 200
    assert b"Add new plant family" in res.data
    pest_names = faker.random_choices(elements=db.session.scalars(sa.select(m.Pest.name)).all(), length=3)
    illness_names = faker.random_choices(elements=db.session.scalars(sa.select(m.Illness.name)).all(), length=3)
    plant_family_data = dict(
        name="test plant family",
        features="test plant family features",
        pests=pest_names,
        illnesses=illness_names,
    )
    res = login_client.post("/plant-family/create", data=plant_family_data, follow_redirects=True)
    assert res.status_code == 200
    assert b"test plant family" in res.data
    plant_family = db.session.get(m.PlantFamily, len(plant_families) + 1)
    assert plant_family.name == plant_family_data["name"]
    assert [pest.name for pest in plant_family.pests].sort() == pest_names.sort()

    # update
    res = login_client.get(f"/plant-family/detail/{plant_family.id}")
    assert res.status_code == 200
    assert b"Edit plant family" in res.data
    assert plant_family.name.encode("utf-8") in res.data
    illness_names = faker.random_choices(elements=db.session.scalars(sa.select(m.Illness.name)).all(), length=3)
    NEW_NAME = "updated plant family name"
    plant_family_data["name"] = NEW_NAME
    plant_family_data["illnesses"] = illness_names
    res = login_client.post(
        f"/plant-family/detail/{plant_family.id}",
        data=plant_family_data,
        follow_redirects=True,
    )
    assert res.status_code == 200
    assert NEW_NAME.encode("utf-8") in res.data
    plant_family = db.session.get(m.PlantFamily, plant_family.id)
    assert plant_family.name == NEW_NAME
    assert [illness.name for illness in plant_family.illnesses].sort() == illness_names.sort()
