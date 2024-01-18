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
from app import s3bucket

bp = Blueprint("pest", __name__, url_prefix="/pest")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    add_form = f.PestForm()
    log(log.INFO, "Get all pests")
    q = request.args.get("q", type=str, default=None)
    where = sa.and_(m.Pest.is_deleted.is_(False))

    if q:
        where = sa.and_(m.Pest.name.ilike(f"%{q}%"), m.Pest.is_deleted.is_(False))

    query = m.Pest.select().where(where).order_by(m.Pest.id.desc())
    count_query = sa.select(sa.func.count()).where(where).select_from(m.Pest)
    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "pest/pests.html",
        pests=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        ).scalars(),
        page=pagination,
        search_query=q,
        add_form=add_form,
    )


@bp.route("/<uuid>/edit", methods=["GET", "POST"])
@login_required
def edit(uuid: str):
    form = f.PestForm()
    pest: m.Pest | None = db.session.scalar(sa.Select(m.Pest).where(m.Pest.uuid == uuid))
    if not pest or pest.is_deleted:
        log(log.ERROR, "Not found pest by uuid: [%s]", uuid)
        flash("Cannot save pest data", "danger")
        return redirect(url_for("pest.get_all"))

    if request.method == "GET":
        form.name.data = pest.name
        form.symptoms.data = pest.symptoms
        form.treatment.data = pest.treatment
        return render_template("pest/edit.html", form=form, pest=pest)

    if form.validate_on_submit() and not db.session.scalar(
        sa.Select(m.Pest.name).where(m.Pest.name == form.name.data, m.Pest.uuid != uuid)
    ):
        pest.name = form.name.data
        pest.symptoms = form.symptoms.data
        pest.treatment = form.treatment.data
        for photo in form.photos.data:
            try:
                pest._photos.append(s3bucket.create_photo(photo, "pests"))
            except TypeError as error:
                log(log.ERROR, "Error with add photo new pest: [%s]", error)
                flash("Error with add photo to new pest", "danger")
                return redirect(url_for("pest.get_all"))

        pest.save()
        return redirect(url_for("pest.get_all"))

    if form.errors:
        log(log.ERROR, "Pest save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
    return redirect(url_for("pest.get_all"))


@bp.route("/create", methods=["POST"])
@login_required
def create():
    form = f.PestForm()

    if form.validate_on_submit() and not db.session.scalar(sa.Select(m.Pest.name).where(m.Pest.name == form.name.data)):
        pest = m.Pest(
            name=form.name.data,
            symptoms=form.symptoms.data,
            treatment=form.treatment.data,
        )
        for photo in form.photos.data:
            try:
                pest._photos.append(s3bucket.create_photo(photo, "pests"))
            except TypeError as error:
                log(log.ERROR, "Error with add photo new pest: [%s]", error)
                flash("Error with add photo to new pest", "danger")
                return redirect(url_for("pest.get_all"))
        log(log.INFO, "Form submitted. Pest: [%s]", pest)
        flash("Pest added!", "success")
        pest.save()
    else:
        log(
            log.ERROR,
            "Error with creating new pest: [%s]",
            form.errors,
        )
        flash("Error with creating new pest", "danger")

    return redirect(url_for("pest.get_all"))


@bp.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete(id: int):
    pest = db.session.get(m.Pest, id)
    if not pest or pest.is_deleted:
        log(log.INFO, "There is no pest with id: [%s]", id)
        flash("There is no such pest", "danger")
        return "no pest", 404

    pest.is_deleted = True
    pest.name = f"{pest.name}-deleted_at: {datetime.now()}"
    pest.plant_families = []
    pest.plant_varieties = []
    db.session.commit()
    log(log.INFO, "Pest deleted. Pest: [%s]", pest)
    return "ok", 200
