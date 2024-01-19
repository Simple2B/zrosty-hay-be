from flask import Blueprint, request, render_template
import sqlalchemy as sa

from app import models as m, db
from app.logger import log


bp = Blueprint("photo", __name__, url_prefix="/photos")


@bp.route("/<uuid>", methods=["GET", "DELETE"])
def delete(uuid: str):
    log(log.INFO, "Delete photo: [%s]", uuid)
    if request.method == "GET":
        return render_template("photo/confirm_delete.html", uuid=uuid)

    photo = db.session.scalar(sa.select(m.Photo).where(m.Photo.uuid == uuid))
    if not photo or photo.is_deleted:
        log(log.ERROR, "Photo not found: [%s]", uuid)
        return "Not found", 404
    photo.is_deleted = True
    db.session.commit()
    return "success", 200
