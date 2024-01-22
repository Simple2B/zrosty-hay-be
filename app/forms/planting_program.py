from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class StepForm(FlaskForm):
    day = IntegerField("day", [DataRequired()], render_kw={"placeholder": "Enter day"})
    instruction = TextAreaField("instruction", [DataRequired()], render_kw={"placeholder": "Enter instruction"})
    step_type_id = SelectField("step_type_id", [DataRequired()], choices=[])


class PlantProgramForm(FlaskForm):
    planting_time = IntegerField("planting_time", [DataRequired()], render_kw={"placeholder": "Enter planting time"})
    harvest_time = IntegerField("harvest_time", [DataRequired()], render_kw={"placeholder": "Enter harvest time"})
