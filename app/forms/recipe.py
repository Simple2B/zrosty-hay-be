from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length
from .photo import UploadPhotoForm


class RecipeForm(UploadPhotoForm, FlaskForm):
    name = StringField("Name", [DataRequired(), Length(1, 64)], render_kw={"placeholder": "Enter name"})
    cooking_time = IntegerField("Cooking Time", [DataRequired()], render_kw={"placeholder": "Enter cooking time"})
    description = TextAreaField("Description", [DataRequired()], render_kw={"placeholder": "Enter description"})
    categories = SelectMultipleField("Categories", choices=[])
