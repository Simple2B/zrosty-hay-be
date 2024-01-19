from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
import sqlalchemy as sa
from app.controllers import create_pagination

from app import models as m, db
from app import forms as f
from app.logger import log
from app import s3bucket

bp = Blueprint("planting_program", __name__, url_prefix="/planting-programs")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    log(log.INFO, "Get all plant varieties")
    q = request.args.get("q", type=str, default=None)
    query = m.PlantVariety.select().order_by(m.PlantVariety.id.desc())
    count_query = sa.select(sa.func.count()).select_from(m.PlantVariety)
    if q:
        query = m.PlantVariety.select().where(m.PlantVariety.name.ilike(f"%{q}%")).order_by(m.PlantVariety.id.desc())
        count_query = sa.select(sa.func.count()).where(m.PlantVariety.name.ilike(f"%{q}%")).select_from(m.PlantVariety)

    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "plant_variety/plant_varieties.html",
        plant_varieties=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = f.PlantFamilyAddForm()
    if request.method == "GET":
        form.plant_family_id.choices = db.session.execute(
            sa.Select(m.PlantFamily.id, m.PlantFamily.name).where(m.PlantFamily.is_deleted.is_(False))
        ).all()

        form.pests.choices = db.session.scalars(sa.Select(m.Pest.name).where(m.Pest.is_deleted.is_(False))).all()
        form.illnesses.choices = db.session.scalars(
            sa.Select(m.Illness.name).where(m.Illness.is_deleted.is_(False))
        ).all()

    if (
        request.method == "POST"
        and form.validate_on_submit()
        and not db.session.scalar(sa.Select(m.PlantVariety.name).where(m.PlantVariety.name == form.name.data))
    ):
        plant_family = db.session.get(m.PlantFamily, form.plant_family_id.data)
        if not plant_family:
            log(
                log.INFO,
                "Error can't find plant_family id:[%d]",
                form.plant_family_id.data,
            )
            flash("Plant family not exist!", "danger")
            return redirect(url_for("plant_variety.get_all"))
        pests = db.session.scalars(sa.Select(m.Pest).where(m.Pest.name.in_(form.pests.data)))
        illness = db.session.scalars(sa.Select(m.Illness).where(m.Illness.name.in_(form.pests.data)))
        plant_variety = m.PlantVariety(
            family=plant_family,
            name=form.name.data,
            features=form.features.data,
            general_info=form.general_info.data,
            temperature_info=form.temperature_info.data,
            watering_info=form.watering_info.data,
            planting_min_temperature=form.planting_min_temperature.data,
            planting_max_temperature=form.planting_max_temperature.data,
            is_moisture_loving=form.is_moisture_loving.data,
            is_sun_loving=form.is_sun_loving.data,
            ground_ph=form.ground_ph.data,
            ground_type=form.ground_type.data,
            can_plant_indoors=form.can_plant_indoors.data,
        )
        plant_variety.pests.extend(pests)
        plant_variety.illnesses.extend(illness)

        for photo in form.photos.data:
            try:
                plant_variety._photos.append(s3bucket.create_photo(photo, "plant_varieties"))
            except TypeError as error:
                log(log.ERROR, "Error with add photo new plant variety: [%s]", error)
                flash("Error with add photo to new plant variety", "danger")
                return redirect(url_for("plant_variety.get_all"))

        flash("Plant Variety added!", "success")
        plant_variety.save()
        log(log.INFO, "Form submitted. Plant Variety: [%s]", plant_variety)
        return redirect(url_for("plant_variety.get_all"))
    if form.errors:
        log(log.INFO, "Form error [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        return redirect(url_for("plant_variety.get_all"))

    return render_template("plant_variety/add_form.html", form=form)


@bp.route("/<uuid>/edit", methods=["GET", "POST"])
@login_required
def edit(uuid: str):
    form = f.PlantVarietyForm()
    plant_variety: m.PlantVariety | None = db.session.scalar(
        sa.Select(m.PlantVariety).where(m.PlantVariety.uuid == uuid)
    )
    if not plant_variety:
        log(log.INFO, "Error can't find plant_variety uuid:[%s]", uuid)
        flash("Plant family not exist!", "danger")
        return redirect(url_for("plant_variety.get_all"))

    if request.method == "GET":
        form.pests.choices = db.session.scalars(sa.Select(m.Pest.name).where(m.Pest.is_deleted.is_(False))).all()
        form.illnesses.choices = db.session.scalars(
            sa.Select(m.Illness.name).where(m.Illness.is_deleted.is_(False))
        ).all()
        form.name.data = plant_variety.name
        form.features.data = plant_variety.features
        form.general_info.data = plant_variety.general_info
        form.temperature_info.data = plant_variety.temperature_info
        form.watering_info.data = plant_variety.watering_info
        form.planting_min_temperature.data = plant_variety.planting_min_temperature
        form.planting_max_temperature.data = plant_variety.planting_max_temperature
        form.is_moisture_loving.data = plant_variety.is_moisture_loving
        form.is_sun_loving.data = plant_variety.is_sun_loving
        form.ground_ph.data = plant_variety.ground_ph
        form.ground_type.data = plant_variety.ground_type
        form.can_plant_indoors.data = plant_variety.can_plant_indoors
        form.pests.data = [pest.name for pest in plant_variety.pests]
        form.illnesses.data = [illness.name for illness in plant_variety.illnesses]

    if request.method == "POST" and form.validate_on_submit():
        if form.name.data and db.session.scalar(
            sa.Select(m.PlantVariety.name).where(m.PlantVariety.name == form.name.data, m.PlantVariety.uuid != uuid)
        ):
            log(log.INFO, "PlantVariety name already exist! [%s]", form.name.data)
            flash("Plan Variety name already exist!", "danger")
            return redirect(url_for("plant_variety.get_all"))

        pests = db.session.scalars(sa.Select(m.Pest).where(m.Pest.name.in_(form.pests.data))).all()
        illness = db.session.scalars(sa.Select(m.Illness).where(m.Illness.name.in_(form.pests.data))).all()
        plant_variety.name = form.name.data
        plant_variety.features = form.features.data
        plant_variety.general_info = form.general_info.data
        plant_variety.temperature_info = form.temperature_info.data
        plant_variety.watering_info = form.watering_info.data
        plant_variety.planting_min_temperature = form.planting_min_temperature.data
        plant_variety.planting_max_temperature = form.planting_max_temperature.data
        plant_variety.is_moisture_loving = form.is_moisture_loving.data
        plant_variety.is_sun_loving = form.is_sun_loving.data
        plant_variety.ground_ph = form.ground_ph.data
        plant_variety.ground_type = form.ground_type.data
        plant_variety.can_plant_indoors = form.can_plant_indoors.data
        plant_variety.pests = pests
        plant_variety.illnesses = illness

        for photo in form.photos.data:
            try:
                plant_variety._photos.append(s3bucket.create_photo(photo, "plant_varieties"))
            except TypeError as error:
                log(log.ERROR, "Error with add photo new plant variety: [%s]", error)
                flash("Error with add photo to new plant variety", "danger")
                return redirect(url_for("plant_variety.get_all"))

        flash("Plant Variety updated!", "success")
        plant_variety.save()
        log(log.INFO, "Form submitted. Plant Variety: [%s]", plant_variety)
        return redirect(url_for("plant_variety.get_all"))
    if form.errors:
        log(log.INFO, "Form error [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        return redirect(url_for("plant_variety.get_all"))

    return render_template("plant_variety/edit_form.html", form=form, plant_variety=plant_variety)
