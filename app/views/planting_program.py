from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

import sqlalchemy as sa

from app import forms as f
from app import models as m
from app.logger import log
from app.database import db

bp = Blueprint("planting_program", __name__, url_prefix="/planting-programs")


@bp.route("/<uuid>/edit", methods=["GET", "POST"])
@login_required
def edit(uuid: str):
    log(log.INFO, "Edit program uuid: [%s]", uuid)
    form = f.PlantingProgramEditForm()

    program = db.session.scalar(sa.select(m.PlantingProgram).where(m.PlantingProgram.uuid == uuid))
    if not program or program.is_deleted:
        flash("Program not found", "danger")
        log(log.ERROR, "Program with uuid: [%s] not found", uuid)
        return redirect(url_for("plant_variety.get_all"))

    if request.method == "POST" and form.validate_on_submit():
        steps_data = tuple(
            zip(
                request.form.getlist("uuid"),
                request.form.getlist("step_type_id"),
                request.form.getlist("day"),
                request.form.getlist("instruction"),
            )
        )
        program.planting_time = form.planting_time.data
        program.harvest_time = form.harvest_time.data
        for step_data in steps_data:
            uuid, step_type_id, day, instruction = step_data
            if uuid:
                program_step = db.session.scalar(sa.select(m.PlantingStep).where(m.PlantingStep.uuid == uuid))
                if not program_step or program_step.is_deleted:
                    log(log.INFO, "Error can't find plant program step uuid:[%d]", uuid)
                    continue
                program_step.step_type_id = int(step_type_id)
                program_step.day = int(day)
                program_step.instruction = instruction
            else:
                step = m.PlantingStep(
                    step_type_id=step_type_id, day=day, instruction=instruction, planting_program_id=program.id
                )
                db.session.add(step)
        db.session.commit()

        return redirect(url_for("plant_variety.programs", uuid=program.plant_variety.uuid))

    step_types = db.session.execute(sa.select(m.PlantingStepType.id, m.PlantingStepType.name)).all()
    form.planting_time.data = program.planting_time
    form.harvest_time.data = program.harvest_time
    steps = []
    for step in program.steps:
        step_form = f.StepEditForm(uuid=step.uuid, day=step.day, instruction=step.instruction)
        step_form.step_type_id.choices = step_types
        step_form.step_type_id.data = step.step_type_id
        steps.append(step_form)

    form.steps = steps

    return render_template("planting_program/edit.html", form=form, uuid=program.uuid)
