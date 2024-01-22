from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
import sqlalchemy as sa
from app.controllers import create_pagination

from app import models as m, db
from app import forms as f
from app.logger import log

bp = Blueprint("planting_step_type", __name__, url_prefix="/planting-step-types")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    log(log.INFO, "Get all planting step types")
    q = request.args.get("q", type=str, default=None)
    where = sa.and_(m.PlantingStepType.is_deleted.is_(False))

    if q:
        where = sa.and_(m.PlantingStepType.name.ilike(f"%{q}%"), m.PlantingStepType.is_deleted.is_(False))

    query = m.PlantingStepType.select().where(where).order_by(m.PlantingStepType.id.desc())
    count_query = sa.select(sa.func.count()).where(where).select_from(m.PlantingStepType)
    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "planting_step_type/planting_step_types.html",
        step_types=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = f.PlantingStepTypeForm()

    if form.validate_on_submit() and not db.session.scalar(
        sa.select(m.PlantingStepType.name).where(m.PlantingStepType.name == form.name.data)
    ):
        step_type = m.PlantingStepType(
            name=form.name.data,
        )

        log(log.INFO, "Form submitted. Planting step type: [%s]", step_type)
        flash("Planting step type added!", "success")
        step_type.save()
        return redirect(url_for("planting_step_type.get_all"))
    if form.errors:
        log(
            log.ERROR,
            "Error with creating new planting step type: [%s]",
            form.errors,
        )
        flash("Error with creating new planting step type", "danger")
        return redirect(url_for("planting_step_type.get_all"))

    return render_template("planting_step_type/add.html", form=form)


@bp.route("/<uuid>/edit", methods=["GET", "POST"])
@login_required
def edit(uuid: str):
    form = f.PlantingStepTypeForm()
    step_type = db.session.scalar(sa.select(m.PlantingStepType).where(m.PlantingStepType.uuid == uuid))
    if not step_type or step_type.is_deleted:
        log(log.ERROR, "Not found planting step type by uuid: [%s]", uuid)
        return "not Found", 404

    if request.method == "GET":
        form.name.data = step_type.name
        return render_template("planting_step_type/edit.html", form=form, step_type=step_type)

    if form.validate_on_submit() and not db.session.scalar(
        sa.Select(m.PlantingStepType.name).where(
            m.PlantingStepType.name == form.name.data, m.PlantingStepType.uuid != uuid
        )
    ):
        step_type.name = form.name.data
        step_type.save()
        return redirect(url_for("planting_step_type.get_all"))

    if form.errors:
        log(log.ERROR, "Planting step type save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
    return redirect(url_for("planting_step_type.get_all"))
