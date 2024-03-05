from flask import Flask
import sqlalchemy as sa
from sqlalchemy import orm
from app import models as m
from app.database import db
from app import forms
from app import schema as s
from .parse_excel import parse_excel
from .parse_json import parse_json


def init(app: Flask):
    # flask cli context setup
    @app.shell_context_processor
    def get_context():
        """Objects exposed here will be automatically available from the shell."""
        return dict(app=app, db=db, m=m, f=forms, s=s, sa=sa, orm=orm)

    @app.cli.command()
    def db_populate():
        """Fill DB by dummy data."""

        with open("test_data.json", "r") as f:
            data = s.TestData.model_validate_json(f.read())
        for plant_family in data.plant_families:
            db.session.add(m.PlantFamily(**plant_family.model_dump()))
        for plant_variety in data.plant_varieties:
            db.session.add(m.PlantVariety(**plant_variety.model_dump()))

        db.session.commit()

        print("DB populated successful")

    @app.cli.command("create-admin")
    def create_admin():
        """Create super admin account"""
        query = m.User.select().where(m.User.email == app.config["ADMIN_EMAIL"])
        if db.session.execute(query).first():
            print(f"User with e-mail: [{app.config['ADMIN_EMAIL']}] already exists")
            return
        m.User(
            username=app.config["ADMIN_USERNAME"],
            email=app.config["ADMIN_EMAIL"],
            password=app.config["ADMIN_PASSWORD"],
            activated=True,
        ).save()
        print("admin created")

    @app.cli.command("add-plants-xlsx")
    def add_plants_from_xlsx():
        """Add plants from excel file to DB."""
        print("Start")
        try:
            parse_excel("plants_data.xlsx", db)
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
        print("Finish")

    @app.cli.command("add-plants-json")
    def add_plants_from_json():
        """Add new plants to DB from plants.json. Use it only for staging db and before"""
        try:
            parse_json("plants.json", db)
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")

        print("Added successful")
