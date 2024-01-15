from flask_wtf import FlaskForm
from wtforms import StringField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Length


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PlantFamilyForm(FlaskForm):
    name = StringField(
        "name",
        [DataRequired(), Length(min=3, max=128)],
    )
    features = StringField("reason", [Length(min=3, max=1024)])
    pests = MultiCheckboxField("pests")
    illnesses = MultiCheckboxField("illnesses")
