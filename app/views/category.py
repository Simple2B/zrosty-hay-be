from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
import sqlalchemy as sa
from app.controllers import create_pagination

from app import models as m, db
from app import forms as f
from app.logger import log

bp = Blueprint("category", __name__, url_prefix="/categories")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    log(log.INFO, "Get all categories")
    q = request.args.get("q", type=str, default=None)
    where = sa.and_(m.Category.is_deleted.is_(False))

    if q:
        where = sa.and_(m.Category.name.ilike(f"%{q}%"), m.Category.is_deleted.is_(False))

    query = m.Category.select().where(where).order_by(m.Category.id.desc())
    count_query = sa.select(sa.func.count()).where(where).select_from(m.Category)
    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "category/categories.html",
        categories=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = f.CategoryForm()

    if form.validate_on_submit() and not db.session.scalar(
        sa.select(m.Category.name).where(m.Category.name == form.name.data)
    ):
        new_category = m.Category(name=form.name.data)

        log(log.INFO, "Form submitted. Category name: [%s]", new_category.name)
        flash("Category added!", "success")
        new_category.save()
        return redirect(url_for("category.get_all"))
    if form.errors:
        log(
            log.ERROR,
            "Error with creating new category: [%s]",
            form.errors,
        )
        flash("Error with creating new category", "danger")
        return redirect(url_for("category.get_all"))

    return render_template("category/add.html", form=form)


@bp.route("/<uuid>/edit", methods=["GET", "POST"])
@login_required
def edit(uuid: str):
    form = f.CategoryForm()
    category = db.session.scalar(sa.select(m.Category).where(m.Category.uuid == uuid))
    if not category or category.is_deleted:
        log(log.ERROR, "Not found category by uuid: [%s]", uuid)
        return "not Found", 404

    if request.method == "GET":
        form.name.data = category.name

        return render_template("category/edit.html", form=form, category=category)

    if form.validate_on_submit() and not db.session.scalar(
        sa.select(m.Category.name).where(m.Category.name == form.name.data, m.Category.uuid != uuid)
    ):
        category.name = form.name.data
        category.save()

        return redirect(url_for("category.get_all"))

    if form.errors:
        log(log.ERROR, "Category save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
    return redirect(url_for("category.get_all"))
