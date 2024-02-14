from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
import sqlalchemy as sa
from app.controllers import create_pagination

from app import models as m, db
from app import forms as f
from app.logger import log
from app import s3bucket

bp = Blueprint("recipe", __name__, url_prefix="/recipes")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    log(log.INFO, "Get all plant recipes")
    q = request.args.get("q", type=str, default=None)
    query = m.Recipe.select().order_by(m.Recipe.id.desc())
    count_query = sa.select(sa.func.count()).select_from(m.Recipe)
    if q:
        query = m.Recipe.select().where(m.Recipe.name.ilike(f"%{q}%")).order_by(m.Recipe.id.desc())
        count_query = sa.select(sa.func.count()).where(m.Recipe.name.ilike(f"%{q}%")).select_from(m.Recipe)

    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "recipe/recipes.html",
        recipes=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = f.RecipeForm()
    form.plant_varieties.choices = db.session.scalars(sa.select(m.PlantVariety.name)).all()
    form.categories.choices = db.session.scalars(sa.select(m.Category.name)).all()
    if (
        request.method == "POST"
        and form.validate_on_submit()
        and not db.session.scalar(sa.select(m.Recipe.name).where(m.Recipe.name == form.name.data))
    ):
        recipe = m.Recipe(
            name=form.name.data,
            description=form.description.data,
            cooking_time=form.cooking_time.data,
            additional_ingredients=form.additional_ingredients.data,
        )

        plant_varieties = db.session.scalars(
            sa.select(m.PlantVariety).where(m.PlantVariety.name.in_(form.plant_varieties.data))
        ).all()
        recipe.plant_varieties = plant_varieties
        categories = db.session.scalars(sa.select(m.Category).where(m.Category.name.in_(form.categories.data))).all()
        recipe.categories = categories

        for photo in form.photos.data:
            try:
                s3_photo = s3bucket.create_photo(photo.stream, folder_name="recipes")
            except TypeError as error:
                log(log.ERROR, "Error with add photo new recipe: [%s]", error)
                flash("Error with add photo to new recipe", "danger")
                return redirect(url_for("recipe.get_all"))
            recipe.photos.append(m.Photo(original_name=photo.filename, **s3_photo.model_dump()))

        flash("Recipe added!", "success")
        recipe.save()
        log(log.INFO, "Form submitted. Recipe: [%s]", recipe)
        return redirect(url_for("recipe.get_all"))
    if form.errors:
        log(log.INFO, "Form error [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        return redirect(url_for("recipe.get_all"))

    return render_template("recipe/form.html", form=form)


@bp.route("/<uuid>/edit", methods=["GET", "POST"])
@login_required
def edit(uuid: str):
    form = f.RecipeForm()
    recipe = db.session.scalar(sa.select(m.Recipe).where(m.Recipe.uuid == uuid))
    if not recipe or recipe.is_deleted:
        log(log.INFO, "Error can't find recipe uuid:[%s]", uuid)
        flash("Recipe not exist!", "danger")
        return redirect(url_for("recipe.get_all"))

    form.plant_varieties.choices = db.session.scalars(sa.select(m.PlantVariety.name)).all()
    form.categories.choices = db.session.scalars(sa.select(m.Category.name)).all()

    if request.method == "POST" and form.validate_on_submit():
        if not db.session.scalar(
            sa.Select(m.Recipe.name).where(m.Recipe.name == form.name.data, m.Recipe.uuid != uuid)
        ):
            flash("Name already exist!", "success")
            return redirect(url_for("recipe.get_all"))
        recipe.name = form.name.data
        recipe.cooking_time = form.cooking_time.data
        recipe.additional_ingredients = form.additional_ingredients.data
        recipe.description = form.description.data
        plant_varieties = db.session.scalars(
            sa.select(m.PlantVariety).where(m.PlantVariety.name.in_(form.plant_varieties.data))
        ).all()
        recipe.plant_varieties = plant_varieties
        categories = db.session.scalars(sa.select(m.Category).where(m.Category.name.in_(form.categories.data))).all()
        recipe.categories = categories

        for photo in form.photos.data:
            try:
                s3_photo = s3bucket.create_photo(photo.stream, folder_name="plant_varieties")
            except TypeError as error:
                log(log.ERROR, "Error with add photo new plant variety: [%s]", error)
                flash("Error with add photo to new plant variety", "danger")
                return redirect(url_for("plant_variety.get_all"))
            recipe.photos.append(m.Photo(original_name=photo.filename, **s3_photo.model_dump()))

        recipe.save()
        flash("Recipe updated!", "success")
        log(log.INFO, "Form submitted. Recipe: [%s]", recipe.name)
        return redirect(url_for("recipe.get_all"))
    if form.errors:
        log(log.INFO, "Form error [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        return redirect(url_for("recipe.get_all"))

    form.name.data = recipe.name
    form.cooking_time.data = recipe.cooking_time
    form.additional_ingredients.data = recipe.additional_ingredients
    form.description.data = recipe.description
    form.plant_varieties.data = [pv.name for pv in recipe.plant_varieties]
    form.categories.data = [c.name for c in recipe.categories]

    return render_template("recipe/form.html", form=form, recipe_uuid=uuid)
