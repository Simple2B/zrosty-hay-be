from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Length

from app import models as m
from app import db


class PlantVarietyForm(FlaskForm):
    plant_family_id = SelectField("plant_family_id", [DataRequired()])
    name = StringField("name", [DataRequired(), Length(1, 64)])
    features = StringField("features", [Length(0, 1024)])
    general_info = StringField("features", [Length(0, 2048)])
    temperature_info = StringField("features", [Length(0, 2048)])
    watering_info = StringField("features", [Length(0, 2048)])
    planting_min_temperature = FloatField("planting_min_temperature")
    planting_max_temperature = FloatField("planting_max_temperature")
    is_moisture_loving = BooleanField("is_moisture_loving")
    is_sun_loving = BooleanField("is_sun_loving")
    ground_ph = IntegerField("ground_ph")
    ground_type = StringField("ground_type")
    can_plant_indoors = BooleanField("can_plant_indoors")

    # illnesses = SelectMultipleField("illnesses", choices=[], validate_choice=False)
    # pests = SelectMultipleField("pests", choices=[], validate_choice=False)
