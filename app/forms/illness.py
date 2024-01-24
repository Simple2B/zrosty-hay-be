from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from .photo import UploadPhotoForm


class IllnessForm(UploadPhotoForm, FlaskForm):
    name = StringField("name", [DataRequired(), Length(min=3, max=128)], render_kw={"placeholder": "Enter name"})
    reason = TextAreaField("reason", [Length(min=0, max=1024)], render_kw={"placeholder": "Enter reason"})
    symptoms = TextAreaField("symptoms", [Length(min=0, max=1024)], render_kw={"placeholder": "Enter symptoms"})
    treatment = TextAreaField("treatment", [Length(min=0, max=1024)], render_kw={"placeholder": "Enter treatment"})
