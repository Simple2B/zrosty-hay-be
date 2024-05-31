from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
import sqlalchemy as sa
from app.controllers import create_pagination

from app import models as m, db
from app import forms as f
from app.logger import log

bp = Blueprint("additional_ingredients", __name__, url_prefix="/additional-ingredients")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    log(log.INFO, "Get all categories")
    q = request.args.get("q", type=str, default=None)
    where = sa.and_(m.AdditionalIngredient.is_deleted.is_(False))

    if q:
        where = sa.and_(m.AdditionalIngredient.name.ilike(f"%{q}%"), m.AdditionalIngredient.is_deleted.is_(False))

    query = m.AdditionalIngredient.select().where(where).order_by(m.AdditionalIngredient.id.desc())
    count_query = sa.select(sa.func.count()).where(where).select_from(m.AdditionalIngredient)
    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "additional_ingredient/additional_ingredients.html",
        additional_ingredients=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = f.AdditionalIngredientForm()

    if form.validate_on_submit() and not db.session.scalar(
        sa.select(m.AdditionalIngredient.name).where(m.AdditionalIngredient.name == form.name.data)
    ):
        additional_ingredient = m.AdditionalIngredient(name=form.name.data)

        log(log.INFO, "Form submitted. additional_ingredient name: [%s]", additional_ingredient.name)
        flash("Additional Ingredient added!", "success")
        additional_ingredient.save()
        return redirect(url_for("additional_ingredients.get_all"))
    if form.errors:
        log(
            log.ERROR,
            "Error with creating new additional_ingredient: [%s]",
            form.errors,
        )
        flash("Error with creating new additional ingredient", "danger")
        return redirect(url_for("additional_ingredients.get_all"))

    return render_template("additional_ingredient/add.html", form=form)


@bp.route("/<uuid>/edit", methods=["GET", "POST"])
@login_required
def edit(uuid: str):
    form = f.AdditionalIngredientForm()
    additional_ingredient = db.session.scalar(
        sa.select(m.AdditionalIngredient).where(m.AdditionalIngredient.uuid == uuid)
    )
    if not additional_ingredient or additional_ingredient.is_deleted:
        log(log.ERROR, "Not found additional_ingredient by uuid: [%s]", uuid)
        return "not Found", 404

    if request.method == "GET":
        form.name.data = additional_ingredient.name

        return render_template(
            "additional_ingredient/edit.html", form=form, additional_ingredient=additional_ingredient
        )

    if form.validate_on_submit() and not db.session.scalar(
        sa.select(m.AdditionalIngredient.name).where(
            m.AdditionalIngredient.name == form.name.data, m.AdditionalIngredient.uuid != uuid
        )
    ):
        additional_ingredient.name = form.name.data
        additional_ingredient.save()

        return redirect(url_for("additional_ingredients.get_all"))

    if form.errors:
        log(log.ERROR, "additional_ingredient save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
    return redirect(url_for("additional_ingredients.get_all"))
