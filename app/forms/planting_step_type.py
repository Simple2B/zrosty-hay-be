from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class PlantingStepTypeForm(FlaskForm):
    name = StringField("name", [DataRequired(), Length(1, 64)], render_kw={"placeholder": "Enter name"})
