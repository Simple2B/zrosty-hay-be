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


bp = Blueprint("pest", __name__, url_prefix="/pest")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    q = request.args.get("q", type=str, default=None)
    query = m.Pest.select().order_by(m.Pest.id)
    count_query = sa.select(sa.func.count()).select_from(m.Pest)
    if q:
        query = m.Pest.select().where(m.Pest.name.ilike(f"%{q}%")).order_by(m.Pest.id)
        count_query = (
            sa.select(sa.func.count())
            .where(m.Pest.name.ilike(f"%{q}%"))
            .select_from(m.Pest)
        )

    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "pest/pests.html",
        pests=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(
                pagination.per_page
            )
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/save", methods=["POST"])
@login_required
def save():
    form = f.UpdatePestForm()

    if form.name.data and db.session.scalar(
        sa.Select(m.Pest.name).where(
            m.Pest.name == form.name.data, m.Pest.id != form.pest_id.data
        )
    ):
        log(log.INFO, "Pest name already exist! [%s]", form.name.data)
        flash("Pest name already exist!", "danger")
        return redirect(url_for("pest.get_all"))

    if form.validate_on_submit():
        query = m.Pest.select().where(m.Pest.id == int(form.pest_id.data))
        pest: m.Pest | None = db.session.scalar(query)
        if not pest:
            log(log.ERROR, "Not found pest by id : [%s]", form.pest_id.data)
            flash("Cannot save pest data", "danger")
            return redirect(url_for("pest.get_all"))
        pest.name = form.name.data
        pest.symptoms = form.symptoms.data
        pest.treatment = form.treatment.data
        # pest.photos = form.photos.data
        pest.save()
        return redirect(url_for("pest.get_all"))

    else:
        log(log.ERROR, "Pest save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        return redirect(url_for("pest.get_all"))


@bp.route("/create", methods=["POST"])
@login_required
def create():
    form = f.PestForm()

    if form.name.data and db.session.scalar(
        sa.Select(m.Pest.name).where(m.Pest.name == form.name.data)
    ):
        log(log.INFO, "Pest name already exist! [%s]", form.name.data)
        flash("Pest name already exist!", "danger")
        return redirect(url_for("pest.get_all"))

    if form.validate_on_submit():
        pest = m.Pest(
            name=form.name.data,
            symptoms=form.symptoms.data,
            treatment=form.treatment.data,
            # photos=form.photos.data,
        )
        log(log.INFO, "Form submitted. Pest: [%s]", pest)
        flash("Pest added!", "success")
        pest.save()
    else:
        log(log.ERROR, "Error with creating new pest")
        flash("Error with creating new pest", "danger")

    return redirect(url_for("pest.get_all"))


@bp.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete(id: int):
    pest = db.session.scalar(m.Pest.select().where(m.Pest.id == id))
    if not pest:
        log(log.INFO, "There is no pest with id: [%s]", id)
        flash("There is no such pest", "danger")
        return "no pest", 404

    db.session.delete(pest)
    db.session.commit()
    log(log.INFO, "Pest deleted. Pest: [%s]", pest)
    flash("Pest deleted!", "success")
    return "ok", 200
