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


bp = Blueprint("plant_variety", __name__, url_prefix="/plant-variety")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    q = request.args.get("q", type=str, default=None)
    query = m.PlantVariety.select().order_by(m.PlantVariety.id)
    count_query = sa.select(sa.func.count()).select_from(m.PlantVariety)
    if q:
        query = (
            m.PlantVariety.select()
            .where(m.PlantVariety.name.ilike(f"%{q}%"))
            .order_by(m.PlantVariety.id)
        )
        count_query = (
            sa.select(sa.func.count())
            .where(m.PlantVariety.name.ilike(f"%{q}%"))
            .select_from(m.PlantVariety)
        )

    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "plant_variety/plant_variety.html",
        plant_varieties=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(
                pagination.per_page
            )
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/save", methods=["POST"])
@login_required
def save():
    form = f.PlantVarietyForm()
    if form.validate_on_submit():
        query = m.PlantVariety.select().where(
            m.PlantVariety.id == int(form.plant_variety_id.data)
        )
        plant_variety: m.PlantVariety | None = db.session.scalar(query)
        if not plant_variety:
            log(
                log.ERROR,
                "Not found plant_variety by id : [%s]",
                form.plant_variety_id.data,
            )
            flash("Cannot save plant_variety data", "danger")
            return redirect(url_for("plant_variety.get_all"))

        query = m.Condition.select().where(
            m.Condition.id == int(form.plant_variety_id.data)
        )

        contition: m.Condition | None = db.session.scalar(query)
        if not plant_variety:
            log(
                log.ERROR,
                "Not found plant_variety by id : [%s]",
                form.plant_variety_id.data,
            )
            flash("Cannot save plant_variety data", "danger")
            return redirect(url_for("plant_variety.get_all"))

        plant_variety.name = form.name.data
        plant_variety.features = form.features.data
        plant_variety.plant_family_id = form.family.data
        plant_variety.illnesses = form.illnesses.data
        plant_variety.pests = form.pests.data

        plant_variety.planting_min_temperature = form.planting_min_temperature.data
        plant_variety.planting_max_temperature = form.planting_max_temperature.data
        plant_variety.is_moisture_loving = form.is_moisture_loving.data
        plant_variety.is_sun_loving = form.is_sun_loving.data
        plant_variety.ground_ph = form.ground_ph.data
        plant_variety.ground_type = form.ground_type.data

        plant_variety.save()

        log(log.INFO, "Form submitted. PlantVariety: [%s]", plant_variety)
        if form.next_url.data:
            return redirect(form.next_url.data)
        return redirect(url_for("plant_variety.get_all"))

    else:
        log(log.ERROR, "User save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        return redirect(url_for("user.get_all"))


@bp.route("/create", methods=["POST"])
@login_required
def create():
    form = f.NewUserForm()
    if form.validate_on_submit():
        condition = m.User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            activated=form.activated.data,
        )
        log(log.INFO, "Form submitted. User: [%s]", condition)
        flash("User added!", "success")
        condition.save()
        return redirect(url_for("user.get_all"))


@bp.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete(id: int):
    u = db.session.scalar(m.User.select().where(m.User.id == id))
    if not u:
        log(log.INFO, "There is no user with id: [%s]", id)
        flash("There is no such user", "danger")
        return "no user", 404

    db.session.delete(u)
    db.session.commit()
    log(log.INFO, "User deleted. User: [%s]", u)
    flash("User deleted!", "success")
    return "ok", 200
