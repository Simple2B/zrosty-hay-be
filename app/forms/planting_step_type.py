from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class PlantingStepTypeForm(FlaskForm):
    name = StringField("Name", [DataRequired(), Length(1, 64)], render_kw={"placeholder": "Enter name"})
    svg_icon = TextAreaField("Svg Icon", [DataRequired()], render_kw={"placeholder": "Svg icon"})


class PlantingStepTypeEditForm(PlantingStepTypeForm):
    color = StringField("Color", [DataRequired(), Length(1, 16)], render_kw={"placeholder": "Enter color"})
