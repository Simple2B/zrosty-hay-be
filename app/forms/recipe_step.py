import uuid

import filetype
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, HiddenField, FileField, ValidationError
from wtforms.validators import DataRequired, Length


class RecipeStepForm(FlaskForm):
    unique_id = str(uuid.uuid4())
    recipe_uuid = HiddenField("Recipe uuid", [DataRequired()])
    name = StringField("Name", [DataRequired(), Length(1, 64)], render_kw={"placeholder": "Enter name"})
    step_number = IntegerField("Step number", [DataRequired()], render_kw={"placeholder": "Enter Step number"})
    instruction = TextAreaField("Description", [DataRequired()], render_kw={"placeholder": "Enter description"})
    photo = FileField("Photo")

    def validate_photo(self, field):
        if not field.data:
            return
        if field.data.content_type == "application/octet-stream":
            return
        is_file = filetype.guess(field.data)
        if not is_file or not filetype.is_image(field.data):
            raise ValidationError("File must be an image")
