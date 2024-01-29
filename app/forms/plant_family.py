from flask_wtf import FlaskForm
from wtforms import StringField, widgets, SelectMultipleField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PlantFamilyForm(FlaskForm):
    name = StringField("name", [DataRequired(), Length(min=3, max=128)], render_kw={"placeholder": "Enter name"})
    features = TextAreaField("features", [Length(min=0, max=1024)], render_kw={"placeholder": "Enter features"})
    type_of = SelectField(
        "type_of",
        choices=[],
        validators=[DataRequired()],
    )
    pests = MultiCheckboxField("pests")
    illnesses = MultiCheckboxField("illnesses")
