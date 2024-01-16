from flask_wtf import FlaskForm
from wtforms import StringField, widgets, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length

from app.models import PlantFamilyType


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PlantFamilyForm(FlaskForm):
    name = StringField(
        "name",
        [DataRequired(), Length(min=3, max=128)],
    )
    features = StringField("reason", [Length(min=3, max=1024)])
    type_of = SelectField(
        "type_of",
        choices=[(type_of.value, type_of.name) for type_of in PlantFamilyType],
        validators=[DataRequired()],
    )
    pests = MultiCheckboxField("pests")
    illnesses = MultiCheckboxField("illnesses")
