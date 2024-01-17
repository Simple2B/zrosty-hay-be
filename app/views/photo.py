from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required
import sqlalchemy as sa
from app.controllers import create_pagination

from app import models as m, db
from app import forms as f
from app.logger import log


bp = Blueprint("photos", __name__, url_prefix="/photos")


def get_all():
    log(log.INFO, "Get all photos")
    # q = request.args.get("q", type=str, default=None)
    # where = sa.and_(m.Photo.is_deleted.is_(False))

    return render_template(
        "photo/photos.html",
    )
