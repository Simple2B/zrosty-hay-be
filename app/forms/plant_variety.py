from flask_wtf import FlaskForm
from wtforms import (
    SelectMultipleField,
    StringField,
    SubmitField,
    ValidationError,
    BooleanField,
    IntegerField,
)
from wtforms.validators import DataRequired

from app import models as m
from app import db


class PlantVarietyForm(FlaskForm):
    next_url = StringField("next_url")
    plant_family_id = IntegerField("plant_family_id", [DataRequired()])
    name = StringField("name", [DataRequired()])
    features = StringField("features")
    illnesses = SelectMultipleField("illnesses", choices=[], validate_choice=False)
    pests = SelectMultipleField("pests", choices=[], validate_choice=False)

    # condition
    planting_min_temperature = IntegerField("planting_min_temperature")
    planting_max_temperature = IntegerField("planting_max_temperature")
    is_moisture_loving = BooleanField("is_moisture_loving")
    is_sun_loving = BooleanField("is_sun_loving")
    ground_ph = IntegerField("ground_ph")
    ground_type = StringField("ground_type")

    submit = SubmitField("Save")
    # TODO: add photos

    def validate_name(self, field):
        query = (
            m.PlantVariety.select()
            .where(m.PlantVariety.name == field.data)
            .where(m.PlantVariety.id != int(self.plant_variety_id.data))
        )
        if db.session.scalar(query) is not None:
            raise ValidationError("Plant with this name already exists.")


class NewPlantVarietyForm(FlaskForm):
    submit = SubmitField("Save")

    def validate_name(self, field):
        query = m.PlantVariety.select().where(m.PlantVariety.name == field.data)
        if db.session.scalar(query) is not None:
            raise ValidationError("Plant with this name already exists")
