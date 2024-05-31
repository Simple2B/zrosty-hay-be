from flask import Blueprint, render_template
from flask_login import login_required
import sqlalchemy as sa

from app import models as m, db
from app.logger import log

bp = Blueprint("recipe_ingredient", __name__, url_prefix="/recipe-ingredient")


@bp.route("/<uuid>", methods=["DELETE"])
@login_required
def delete(uuid: str):
    """htmx"""
    ingredient = db.session.scalar(sa.select(m.RecipeIngredient).where(m.RecipeIngredient.uuid == uuid))
    if not ingredient:
        log(log.ERROR, "Ingredient not found. uuid: [%s]", uuid)
        return render_template("toast.html", message="Ingredient not found.", category="danger")
    db.session.delete(ingredient)
    db.session.commit()

    return render_template("toast.html", message="Ingredient deleted successful.", category="success")
