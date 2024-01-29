from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
import sqlalchemy as sa
from app.controllers import create_pagination

from app import models as m, db
from app import forms as f
from app.logger import log

bp = Blueprint("plant_category", __name__, url_prefix="/plant-category")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    log(log.INFO, "Get all planting step types")
    q = request.args.get("q", type=str, default=None)
    where = sa.and_(m.PlantCategory.is_deleted.is_(False))

    if q:
        where = sa.and_(m.PlantCategory.name.ilike(f"%{q}%"), m.PlantCategory.is_deleted.is_(False))

    query = m.PlantCategory.select().where(where).order_by(m.PlantCategory.id.desc())
    count_query = sa.select(sa.func.count()).where(where).select_from(m.PlantCategory)
    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "plant_category/categories.html",
        categories=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = f.PlantCategoryForm()

    if form.validate_on_submit() and not db.session.scalar(
        sa.select(m.PlantCategory.name).where(m.PlantCategory.name == form.name.data)
    ):
        step_type = m.PlantCategory(
            name=form.name.data,
            svg_icon=form.svg_icon.data,
        )

        log(log.INFO, "Form submitted. Planting step type: [%s]", step_type)
        flash("Planting step type added!", "success")
        step_type.save()
        return redirect(url_for("plant_category.get_all"))
    if form.errors:
        log(
            log.ERROR,
            "Error with creating new planting step type: [%s]",
            form.errors,
        )
        flash("Error with creating new planting step type", "danger")
        return redirect(url_for("plant_category.get_all"))

    return render_template("plant_category/add.html", form=form)


@bp.route("/<uuid>/edit", methods=["GET", "POST"])
@login_required
def edit(uuid: str):
    form = f.PlantCategoryForm()
    category = db.session.scalar(sa.select(m.PlantCategory).where(m.PlantCategory.uuid == uuid))
    if not category or category.is_deleted:
        log(log.ERROR, "Not found planting step type by uuid: [%s]", uuid)
        return "not Found", 404

    if request.method == "GET":
        form.name.data = category.name
        form.svg_icon.data = category.svg_icon
        return render_template("plant_category/edit.html", form=form, category=category)

    if form.validate_on_submit() and not db.session.scalar(
        sa.select(m.PlantCategory.name).where(m.PlantCategory.name == form.name.data, m.PlantCategory.uuid != uuid)
    ):
        category.name = form.name.data
        category.svg_icon = form.svg_icon.data
        category.save()
        return redirect(url_for("plant_category.get_all"))

    if form.errors:
        log(log.ERROR, "Planting step type save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
    return redirect(url_for("plant_category.get_all"))
