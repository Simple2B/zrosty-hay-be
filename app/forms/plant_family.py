from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Length
import sqlalchemy as sa

from app import models as m
from app import db


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PlantFamilyForm(FlaskForm):
    # next_url = StringField("next_url")
    # pest_id = StringField("pest_id")
    name = StringField(
        "name",
        [DataRequired(), Length(min=3, max=128)],
    )
    features = StringField("reason", [Length(min=3, max=1024)])
    pests = MultiCheckboxField("pests")
    illnesses = MultiCheckboxField("illnesses")

    # db.session.scalars(sa.Select(m.Pest.id, m.Pest.name)).all()

    # photos = MultipleFileField("photos")
