import filetype
from flask_wtf import FlaskForm
from wtforms import MultipleFileField, ValidationError
from wtforms.validators import DataRequired


class UploadPhotoForm(FlaskForm):
    photos = MultipleFileField("photos", [DataRequired()])

    def validate_photos(self, field):
        for file in field.data:
            is_file = filetype.guess(file)
            if not is_file or not filetype.is_image(file):
                raise ValidationError("File must be an image")
