from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, Form, FieldList, FormField
from wtforms.validators import DataRequired


class StepForm(Form):
    day = IntegerField("day", [DataRequired()])
    instruction = StringField("instruction", [DataRequired()])


class PlantProgramForm(FlaskForm):
    planting_time = IntegerField("planting_time", [DataRequired()], render_kw={"placeholder": "Enter planting time"})
    harvest_time = IntegerField("harvest_time", [DataRequired()], render_kw={"placeholder": "Enter harvest time"})

    steps = FieldList(FormField(StepForm))
