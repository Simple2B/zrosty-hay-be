from flask import Blueprint, render_template
from flask_login import login_required

from app import forms as f
from app.logger import log

bp = Blueprint("planting_program", __name__, url_prefix="/planting-programs")


@bp.route("/", methods=["GET"])
@login_required
def add_step():
    log(log.INFO, "Add step view")
    form = f.StepForm()
    return render_template("planting_program/step_form.html", form=form)
