from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length
from .photo import UploadPhotoForm


class RecipeForm(UploadPhotoForm, FlaskForm):
    name = StringField("Name", [DataRequired(), Length(1, 64)], render_kw={"placeholder": "Enter name"})
    step_number = IntegerField("Step number", [DataRequired()], render_kw={"placeholder": "Enter Step number"})
    instruction = TextAreaField("Description", [DataRequired()], render_kw={"placeholder": "Enter description"})
