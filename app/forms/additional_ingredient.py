from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class AdditionalIngredientForm(FlaskForm):
    name = StringField("Name", [DataRequired(), Length(1, 128)], render_kw={"placeholder": "Enter name"})
