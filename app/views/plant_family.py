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
    query = m.PlantFamily.select().order_by(m.PlantFamily.id)
    count_query = sa.select(sa.func.count()).select_from(m.PlantFamily)
    if q:
        query = (
            m.PlantFamily.select()
            .where(m.PlantFamily.name.ilike(f"%{q}%"))
            .order_by(m.PlantFamily.id)
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
    if request.method == "POST":
        if form.validate_on_submit():
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
    plant_family = db.session.get(m.PlantFamily, plant_family_id)
    if not plant_family:
        log(log.INFO, "Error can't find illness id:[%d]", plant_family_id)
        return "No Illness", 404
    if request.method == "POST":
        if form.validate_on_submit():
            # TODO
            # illness.name = form.name.data
            # illness.reason = form.reason.data
            # illness.symptoms = form.symptoms.data
            # illness.treatment = form.treatment.data
            log(log.INFO, "Illness updated! [%s]", plant_family)
            flash("Illness updated!", "success")
            # plant_family.save()
        if form.errors:
            log(log.INFO, "Form error Illness! [%s]", form.errors)
            flash(f"{form.errors}", "danger")
        return redirect(url_for("illness.get_all"))

    form.name.data = plant_family.name
    form.features.data = plant_family.features
    # form.pests.select =
    return render_template(
        "plant_family/modal_form.html",
        form=form,
    )


# @bp.route("/delete/<int:illness_id>", methods=["GET", "DELETE"])
# @login_required
# def delete(illness_id: int):
#     illness = db.session.get(m.Illness, illness_id)
#     if not illness:
#         log(log.INFO, "Error can't find illness id:[%d]", illness_id)
#         return "No Illness", 404

#     if request.method == "DELETE":
#         db.session.delete(illness)
#         db.session.commit()
#         log(log.INFO, "Illness deleted. id: [%d]", illness_id)
#         return "success", 200

#     return render_template("illness/confirm_delete.html", illness_id=illness_id)
