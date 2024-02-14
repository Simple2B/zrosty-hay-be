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
    if (
        request.method == "POST"
        and form.validate_on_submit()
        and not db.session.scalar(sa.select(m.Recipe.name).where(m.Recipe.name == form.name.data))
    ):
        # categories = db.session.scalars(
        #     sa.select(m.PlantCategory).where(
        #         m.PlantCategory.name.in_(form.categories.data),
        #         m.PlantCategory.id.not_in([category.id for category in family_categories]),
        #     )
        # ).all()
        # pests = db.session.scalars(sa.select(m.Pest).where(m.Pest.name.in_(form.pests.data)))
        # illness = db.session.scalars(sa.select(m.Illness).where(m.Illness.name.in_(form.pests.data)))
        recipe = m.Recipe(
            name=form.name.data,
            description=form.description.data,
            cooking_time=form.cooking_time.data,
            additional_ingredients=form.additional_ingredients.data,
        )

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

    if request.method == "GET":
        form.name.data = recipe.name
        form.cooking_time.data = recipe.cooking_time
        form.additional_ingredients.data = recipe.additional_ingredients
        form.description.data = recipe.description

    if (
        request.method == "POST"
        and form.validate_on_submit()
        and not db.session.scalar(
            sa.Select(m.Recipe.name).where(m.Recipe.name == form.name.data, m.Recipe.uuid != uuid)
        )
    ):
        recipe.name = form.name.data
        recipe.cooking_time = form.cooking_time.data
        recipe.additional_ingredients = form.additional_ingredients.data
        recipe.description = form.description.data

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

    return render_template("recipe/form.html", form=form, recipe_uuid=uuid)


# @bp.route("/<uuid>/programs", methods=["GET"])
# @login_required
# def programs(uuid: str):
#     plant_variety = db.session.scalar(sa.select(m.PlantVariety).where(m.PlantVariety.uuid == uuid))
#     if not plant_variety:
#         log(log.INFO, "Error can't find plant_variety uuid:[%s]", uuid)
#         flash("Plant family not exist!", "danger")
#         return redirect(url_for("plant_variety.get_all"))

#     programs = plant_variety.programs

#     return render_template("plant_variety/plant_variety_programs.html", programs=programs, uuid=uuid)


# @bp.route("/<uuid>/programs/add", methods=["GET", "POST"])
# @login_required
# def add_program(uuid: str):
#     plant_variety = db.session.scalar(sa.select(m.PlantVariety).where(m.PlantVariety.uuid == uuid))
#     if not plant_variety:
#         log(log.INFO, "Error can't find plant_variety uuid:[%s]", uuid)
#         flash("Plant family not exist!", "danger")
#         return redirect(url_for("plant_variety.get_all"))

#     form = f.PlantProgramForm()
#     if request.method == "POST" and form.validate_on_submit():
#         new_program = m.PlantingProgram(
#             planting_time=form.planting_time.data, harvest_time=form.harvest_time.data, plant_variety=plant_variety
#         )
#         steps_data = tuple(
#             zip(request.form.getlist("step_type_id"), request.form.getlist("day"), request.form.getlist("instruction"))
#         )
#         for step in steps_data:
#             step_type_id, day, instruction = step
#             step_type = db.session.get(m.PlantingStepType, step_type_id)
#             if not step_type:
#                 log(log.ERROR, "can't find step type step_type_id:[%s]", step_type_id)
#                 flash("Error can't find step type", "danger")
#                 return redirect(url_for("plant_variety.programs", uuid=uuid))

#             new_step = m.PlantingStep(day=day, instruction=instruction, step_type=step_type)
#             new_program.steps.append(new_step)

#         new_program.save()

#         return redirect(url_for("plant_variety.programs", uuid=uuid))
#     if form.errors:
#         flash(f"Form error: {form.errors}", "danger")

#     return render_template("planting_program/add.html", form=form, uuid=uuid)
