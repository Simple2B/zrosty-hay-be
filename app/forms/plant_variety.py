from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SelectField,
    SelectMultipleField,
    TextAreaField,
    DecimalField,
)
from wtforms.validators import DataRequired, Length
from .photo import UploadPhotoForm
from app.models import CareType


class PlantVarietyForm(UploadPhotoForm, FlaskForm):
    name = StringField("name", [DataRequired(), Length(1, 64)], render_kw={"placeholder": "Enter name"})
    features = TextAreaField("features", [Length(0, 1024)], default="", render_kw={"placeholder": "Enter features"})
    general_info = TextAreaField(
        "general_info", [Length(0, 2048)], default="", render_kw={"placeholder": "Enter general info"}
    )
    temperature_info = TextAreaField(
        "temperature_info", [Length(0, 2048)], default="", render_kw={"placeholder": "Enter temperature info"}
    )
    watering_info = TextAreaField(
        "watering_info", [Length(0, 2048)], default="", render_kw={"placeholder": "Enter watering info"}
    )
    min_temperature = DecimalField(
        "min_temperature", [DataRequired()], render_kw={"placeholder": "Enter min temperature"}
    )
    max_temperature = DecimalField(
        "max_temperature", [DataRequired()], render_kw={"placeholder": "Enter max temperature"}
    )
    is_moisture_loving = BooleanField("is_moisture_loving")
    is_sun_loving = BooleanField("is_sun_loving")
    ground_ph = DecimalField("ground_ph", render_kw={"placeholder": "Enter ground ph"}, default=0)
    ground_type = StringField("ground_type", default="", render_kw={"placeholder": "Enter ground type"})
    can_plant_indoors = BooleanField("can_plant_indoors")

    min_size = DecimalField("min_size", [DataRequired()], render_kw={"placeholder": "Enter min size"})
    max_size = DecimalField("max_size", [DataRequired()], render_kw={"placeholder": "Enter max size"})
    humidity_percentage = DecimalField(
        "humidity_percentage", render_kw={"placeholder": "Enter humidity percentage"}, default=0
    )
    water_volume = DecimalField("water_volume", render_kw={"placeholder": "Enter water volume"}, default=0)

    care_type = SelectField("care_type", [DataRequired()], choices=[(care.name, care.value) for care in CareType])

    categories = SelectMultipleField("categories", choices=[], validate_choice=False)
    pests = SelectMultipleField("pests", choices=[], validate_choice=False)
    illnesses = SelectMultipleField("illnesses", choices=[], validate_choice=False)


class PlantFamilyAddForm(PlantVarietyForm):
    plant_family_id = SelectField(
        "plant_family_id",
        [DataRequired()],
        validate_choice=False,
    )
