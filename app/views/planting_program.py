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
def add_step():
    form = f.StepForm()
    return render_template("planting_program/step_form.html", form=form)
