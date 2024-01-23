from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    FloatField,
    SelectField,
    SelectMultipleField,
    widgets,
)
from wtforms.validators import DataRequired, Length
from .photo import UploadPhotoForm
from app.models import CareType


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PlantVarietyForm(UploadPhotoForm, FlaskForm):
    name = StringField("name", [DataRequired(), Length(1, 64)])
    features = StringField("features", [Length(0, 1024)], default="")
    general_info = StringField("general_info", [Length(0, 2048)], default="")
    temperature_info = StringField("temperature_info", [Length(0, 2048)], default="")
    watering_info = StringField("watering_info", [Length(0, 2048)], default="")
    min_temperature = FloatField("min_temperature")
    max_temperature = FloatField("max_temperature")
    is_moisture_loving = BooleanField("is_moisture_loving")
    is_sun_loving = BooleanField("is_sun_loving")
    ground_ph = FloatField("ground_ph")
    ground_type = StringField("ground_type", [Length(0, 256)], default="")
    can_plant_indoors = BooleanField("can_plant_indoors")

    min_size = FloatField("min_size")
    max_size = FloatField("max_size")
    humidity_percentage = FloatField("humidity_percentage")
    water_volume = FloatField("water_volume")

    care_type = SelectField("care_type", [DataRequired()], choices=[(care.name, care.value) for care in CareType])

    pests = MultiCheckboxField("pests", choices=[], validate_choice=False)
    illnesses = MultiCheckboxField("illnesses", choices=[], validate_choice=False)


class PlantFamilyAddForm(PlantVarietyForm):
    plant_family_id = SelectField(
        "plant_family_id",
        [DataRequired()],
        validate_choice=False,
    )
