from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from .photo import UploadPhotoForm


class IllnessForm(UploadPhotoForm, FlaskForm):
    name = StringField(
        "name",
        [DataRequired(), Length(min=3, max=128)],
    )
    reason = StringField("reason", [Length(min=3, max=1024)])
    symptoms = StringField("symptoms", [Length(min=3, max=1024)])
    treatment = StringField("treatment", [Length(min=3, max=1024)])
