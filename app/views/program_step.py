from flask import Blueprint, render_template, request
from flask_login import login_required

import sqlalchemy as sa

from app import forms as f
from app import models as m
from app.logger import log
from app.database import db

bp = Blueprint("program_step", __name__, url_prefix="/program-steps")


@bp.route("/", methods=["GET"])
@login_required
def add():
    log(log.INFO, "Add step view")
    form = f.StepForm()
    form.step_type_id.choices = db.session.execute(sa.select(m.PlantingStepType.id, m.PlantingStepType.name)).all()
    return render_template("program_step/form.html", form=form)


@bp.route("/<uuid>/delete", methods=["GET", "DELETE"])
@login_required
def delete(uuid: str):
    log(log.INFO, "Delete program step uuid: [%s]", uuid)
    step = db.session.scalar(sa.select(m.PlantingStep).where(m.PlantingStep.uuid == uuid))
    if not step or step.is_deleted:
        log(log.INFO, "Error can't find program step uuid:[%d]", uuid)
        return "No step", 404

    if request.method == "DELETE":
        step.is_deleted = True
        db.session.commit()
        log(log.INFO, "Program step deleted. id: [%d]", uuid)
        return "success", 200

    return render_template("program_step/confirm_delete.html", uuid=uuid)
