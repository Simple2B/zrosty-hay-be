from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class PlantCategoryForm(FlaskForm):
    name = StringField("Name", [DataRequired(), Length(1, 64)], render_kw={"placeholder": "Enter name"})
    svg_icon = TextAreaField("Svg Icon", [DataRequired()], render_kw={"placeholder": "Add Icon"})
