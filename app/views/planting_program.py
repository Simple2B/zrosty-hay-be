from flask import Blueprint, render_template
from flask_login import login_required

import sqlalchemy as sa

from app import forms as f
from app import models as m
from app.logger import log
from app.database import db

bp = Blueprint("planting_program", __name__, url_prefix="/planting-programs")


@bp.route("/", methods=["GET"])
@login_required
def add_step():
    log(log.INFO, "Add step view")
    form = f.StepForm()
    form.step_type_id.choices = db.session.execute(sa.select(m.PlantingStepType.id, m.PlantingStepType.name)).all()
    return render_template("planting_program/step_form.html", form=form)
