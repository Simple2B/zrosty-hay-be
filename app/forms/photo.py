import filetype
from flask_wtf import FlaskForm
from wtforms import MultipleFileField, ValidationError


class UploadPhotoForm(FlaskForm):
    photos = MultipleFileField("photos", default=[])

    def validate_photos(self, field):
        for file in field.data:
            if file.content_type == "application/octet-stream":
                field.data = []
                return
            is_file = filetype.guess(file)
            if not is_file or not filetype.is_image(file):
                raise ValidationError("File must be an image")
