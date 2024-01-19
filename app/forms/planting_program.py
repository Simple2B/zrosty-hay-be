from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


class PlantProgramForm(FlaskForm):
    planting_time = IntegerField("planting_time", [DataRequired()])
    harvest_time = IntegerField("harvest_time", [DataRequired()])
