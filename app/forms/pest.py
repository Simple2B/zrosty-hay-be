from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    MultipleFileField,
)
from wtforms.validators import DataRequired, Length

from app import models as m
from app import db


class PestForm(FlaskForm):
    # next_url = StringField("next_url")
    # pest_id = StringField("pest_id")
    name = StringField(
        "name",
        [DataRequired(), Length(min=3, max=128)],
    )
    symptoms = StringField("symptoms", [Length(min=3, max=1024)])
    treatment = StringField("treatment", [Length(min=3, max=1024)])
    # plant_families = SelectMultipleField(
    #     "plant_families", choices=[], validate_choice=False
    # )
    # plant_varieties = SelectMultipleField(
    #     "plant_varieties", choices=[], validate_choice=False
    # )

    photos = MultipleFileField("photos")


class UpdatePestForm(PestForm):
    pest_id = StringField("pest_id", [DataRequired()])
