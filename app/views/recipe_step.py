from flask import Blueprint, render_template
from flask_login import login_required
import sqlalchemy as sa

from app import models as m, db
from app import forms as f
from app.logger import log
from app import s3bucket

bp = Blueprint("recipe_step", __name__, url_prefix="/recipes-step")


@bp.route("/<recipe_uuid>/step-form", methods=["GET"])
@login_required
def get_step_form(recipe_uuid: str):
    """htmx request"""
    log(log.INFO, "Get recipe step form")
    reciepe = db.session.scalar(sa.select(m.Recipe).where(m.Recipe.uuid == recipe_uuid))
    if not reciepe or reciepe.is_deleted:
        log(log.INFO, "Error can't find recipe uuid:[%s]", recipe_uuid)
        return render_template("toast.html", category="danger", message="Recipe not exist!")
    form = f.RecipeStepForm(recipe_uuid=recipe_uuid)
    return render_template("recipe_step/form.html", form=form)


@bp.route("/add-step", methods=["POST"])
@login_required
def add_step():
    """htmx request"""
    log(log.INFO, "Add recipe step")
    form = f.RecipeStepForm()
    if not form.validate_on_submit():
        log(log.INFO, "Form error [%s]", form.errors)
        return render_template("toast.html", category="danger", message="Form error [%s]")

    recipe = db.session.scalar(sa.select(m.Recipe).where(m.Recipe.uuid == form.recipe_uuid.data))

    if not recipe or recipe.is_deleted:
        log(log.INFO, "Error can't find recipe uuid:[%s]", form.recipe_uuid.data)
        return render_template("toast.html", category="danger", message="Recipe not exist!")

    step = m.RecipeStep(
        name=form.name.data,
        step_number=form.step_number.data,
        instruction=form.instruction.data,
        recipe=recipe,
    )
    photo = form.photo.data
    if photo:
        try:
            s3_photo = s3bucket.create_photo(photo.stream, folder_name="pests")
        except TypeError as error:
            log(log.ERROR, "Error with add photo new pest: [%s]", error)
            return render_template("toast.html", category="danger", message="Error with add photo new pest")
        step.photo = m.Photo(original_name=photo.filename, **s3_photo.model_dump())

    step.save()
    log(log.INFO, "Form submitted. Step: [%s]", step)
    return render_template("recipe_step/step.html", recipe_step=step)


@bp.route("/<step_uuid>/edit", methods=["GET"])
@login_required
def get_edit_step_form(step_uuid: str):
    """htmx request"""
    log(log.INFO, "Edit recipe step")
    step = db.session.scalar(sa.select(m.RecipeStep).where(m.RecipeStep.uuid == step_uuid))
    if not step or step.is_deleted:
        log(log.INFO, "Error can't find step uuid:[%s]", step_uuid)
        return render_template("toast.html", category="danger", message="Step not found!")

    form = f.RecipeStepForm(recipe_uuid=step.recipe.uuid, **step.__dict__)
    return render_template("recipe_step/edit_form.html", form=form, step_uuid=step_uuid)


@bp.route("/<step_uuid>/edit", methods=["POST"])
@login_required
def edit_step(step_uuid: str):
    """htmx request"""
    log(log.INFO, "Edit recipe step")
    form = f.RecipeStepForm()
    step = db.session.scalar(sa.select(m.RecipeStep).where(m.RecipeStep.uuid == step_uuid))
    if not form.validate_on_submit():
        log(log.INFO, "Form error [%s]", form.errors)
        return render_template("toast.html", category="danger", message="Form error [%s]")
    step.name = form.name.data
    step.step_number = form.step_number.data
    step.instruction = form.instruction.data
    photo = form.photo.data
    if photo:
        try:
            s3_photo = s3bucket.create_photo(photo.stream, folder_name="pests")
        except TypeError as error:
            log(log.ERROR, "Error with add photo new pest: [%s]", error)
            return render_template("toast.html", category="danger", message="Error with add photo new pest")
        step.photo = m.Photo(original_name=photo.filename, **s3_photo.model_dump())

    step.save()
    return render_template("recipe_step/step.html", form=form, recipe_step=step)


@bp.route("/<step_uuid>", methods=["DELETE"])
@login_required
def delete(step_uuid: str):
    """htmx request"""
    log(log.INFO, "Delete recipe step")

    step = db.session.scalar(sa.select(m.RecipeStep).where(m.RecipeStep.uuid == step_uuid))

    if not step or step.is_deleted:
        log(log.INFO, "Error can't find recipe uuid:[%s]", step_uuid)
        return render_template("toast.html", category="danger", message="Step not found!")

    step.as_deleted()
    log(log.INFO, "Form submitted. Step: [%s]", step)
    return render_template("toast.html", category="success", message="Step deleted!")
