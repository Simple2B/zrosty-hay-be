from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    MultipleFileField,
)
from wtforms.validators import DataRequired, Length


class IllnessForm(FlaskForm):
    name = StringField(
        "name",
        [DataRequired(), Length(min=3, max=128)],
    )
    reason = StringField("reason", [Length(min=3, max=1024)])
    symptoms = StringField("symptoms", [Length(min=3, max=1024)])
    treatment = StringField("treatment", [Length(min=3, max=1024)])

    photos = MultipleFileField("photos")
