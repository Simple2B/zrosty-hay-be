import filetype

from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, ValidationError
from wtforms.validators import DataRequired, Length


class PestForm(FlaskForm):
    name = StringField(
        "name",
        [DataRequired(), Length(min=3, max=128)],
    )
    symptoms = StringField("symptoms", [Length(min=3, max=1024)])
    treatment = StringField("treatment", [Length(min=3, max=1024)])

    photos = MultipleFileField("photos", default=[])

    def validate_photos(self, field):
        for file in field.data:
            if file.content_type == "application/octet-stream":
                field.data = []
                return
            is_file = filetype.guess(file)
            if not is_file or not filetype.is_image(file):
                raise ValidationError("File must be an image")


class UpdatePestForm(PestForm):
    pest_id = StringField("pest_id", [DataRequired()])
