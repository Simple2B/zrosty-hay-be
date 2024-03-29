import filetype
import pytest
from dotenv import load_dotenv
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, db
from app import models as m
from app import schema as s
from test_flask.utils import login, register
from .db import FakeData, create_plant_varieties, get_plant_families, create_planting_step_type
from app import s3bucket

load_dotenv("test_flask/test.env")


@pytest.fixture()
def app():
    app = create_app("testing")
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture()
def client(app: Flask, mocker):
    mocker.patch.object(s3bucket, "create_photo", return_value=s.S3Photo(uuid="123", url_path="test_path"))
    mocker.patch.object(filetype, "guess", return_value=True)
    mocker.patch.object(filetype, "is_image", return_value=True)
    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()

        db.drop_all()
        db.create_all()
        register()

        yield client
        db.drop_all()
        app_ctx.pop()


@pytest.fixture()
def runner(app, client):
    from app import commands

    commands.init(app)

    yield app.test_cli_runner()


@pytest.fixture
def populate(client: FlaskClient):
    NUM_TEST_USERS = 100
    for i in range(NUM_TEST_USERS):
        m.User(
            username=f"user{i+1}",
            email=f"user{i+1}@mail.com",
        ).save(False)
    db.session.commit()
    yield client


@pytest.fixture
def add_fake_data() -> FakeData:
    return FakeData(
        plant_families=get_plant_families(),
        plant_varieties=create_plant_varieties(),
        planting_step_types=create_planting_step_type(),
    )


@pytest.fixture
def login_client(client: FlaskClient):
    login(client)
    yield client
