from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required
import sqlalchemy as sa
from app.controllers import create_pagination

from app import models as m, db
from app import forms as f
from app.logger import log


bp = Blueprint("plant_family", __name__, url_prefix="/plant-family")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    q = request.args.get("q", type=str, default=None)
    query = m.PlantFamily.select().order_by(m.PlantFamily.id.desc())
    count_query = sa.select(sa.func.count()).select_from(m.PlantFamily)
    if q:
        query = (
            m.PlantFamily.select()
            .where(m.PlantFamily.name.ilike(f"%{q}%"))
            .order_by(m.PlantFamily.id.desc())
        )
        count_query = (
            sa.select(sa.func.count())
            .where(m.PlantFamily.name.ilike(f"%{q}%"))
            .select_from(m.PlantFamily)
        )

    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "plant_family/plant_families.html",
        plant_families=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(
                pagination.per_page
            )
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = f.PlantFamilyForm()
    form.pests.choices = db.session.scalars(sa.Select(m.Pest.name)).all()
    form.illnesses.choices = db.session.scalars(sa.Select(m.Illness.name)).all()

    if form.name.data and db.session.scalar(
        sa.Select(m.PlantFamily.name).where(m.PlantFamily.name == form.name.data)
    ):
        log(log.INFO, "PlantFamily name already exist! [%s]", form.name.data)
        flash("Plan Family name already exist!", "danger")
        return redirect(url_for("plant_family.get_all"))

    if request.method == "POST" and form.validate_on_submit():
        pests = db.session.scalars(
            sa.Select(m.Pest).where(m.Pest.name.in_(form.pests.data))
        )
        illness = db.session.scalars(
            sa.Select(m.Illness).where(m.Illness.name.in_(form.pests.data))
        )
        plant_family = m.PlantFamily(name=form.name.data, features=form.name.data)
        plant_family.pests.extend(pests)
        plant_family.illnesses.extend(illness)
        flash("PlantFamily added!", "success")
        plant_family.save()
        log(log.INFO, "Form submitted. PlantFamily: [%s]", plant_family)
        return redirect(url_for("plant_family.get_all"))
    if form.errors:
        log(log.INFO, "Form error [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        return redirect(url_for("plant_family.get_all"))

    return render_template("plant_family/modal_form.html", form=form)


@bp.route("/detail/<int:plant_family_id>", methods=["GET", "POST"])
@login_required
def detail(plant_family_id: int):
    form = f.PlantFamilyForm()
    form.pests.choices = db.session.scalars(sa.Select(m.Pest.name)).all()
    form.illnesses.choices = db.session.scalars(sa.Select(m.Illness.name)).all()

    if form.name.data and db.session.scalar(
        sa.Select(m.PlantFamily.name).where(
            m.PlantFamily.name == form.name.data, m.PlantFamily.id != plant_family_id
        )
    ):
        log(log.INFO, "PlantFamily name already exist! [%s]", form.name.data)
        flash("Plan Family name already exist!", "danger")
        return redirect(url_for("plant_family.get_all"))

    plant_family = db.session.get(m.PlantFamily, plant_family_id)

    if not plant_family:
        log(log.INFO, "Error can't find plant_family id:[%d]", plant_family_id)
        return "No Plant family", 404

    if request.method == "POST":
        if form.validate_on_submit():
            plant_family.name = form.name.data
            plant_family.features = form.features.data

            new_pests = db.session.scalars(
                sa.Select(m.Pest).where(m.Pest.name.in_(form.pests.data))
            ).all()

            new_illnesses = db.session.scalars(
                sa.Select(m.Illness).where(m.Illness.name.in_(form.illnesses.data))
            ).all()

            plant_family.pests = new_pests
            plant_family.illnesses = new_illnesses
            log(log.INFO, "Plant_family updated! [%s]", plant_family)
            flash("Plant family updated!", "success")
            plant_family.save()
        if form.errors:
            log(log.INFO, "Form error Plant family! [%s]", form.errors)
            flash(f"{form.errors}", "danger")
        return redirect(url_for("plant_family.get_all"))

    form.name.data = plant_family.name
    form.features.data = plant_family.features
    form.pests.data = [pest.name for pest in plant_family.pests]
    form.illnesses.data = [illness.name for illness in plant_family.illnesses]
    return render_template(
        "plant_family/modal_form.html", form=form, plant_family_id=plant_family.id
    )
