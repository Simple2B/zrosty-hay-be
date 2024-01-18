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


bp = Blueprint("illness", __name__, url_prefix="/illness")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    q = request.args.get("q", type=str, default=None)
    where = sa.and_(m.Illness.is_deleted.is_(False))
    if q:
        where = sa.and_(m.Illness.is_deleted.is_(False), m.Illness.name.ilike(f"%{q}%"))

    query = m.Illness.select().where(where).order_by(m.Illness.id.desc())
    count_query = sa.select(sa.func.count()).where(where).select_from(m.Illness)
    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "illness/illnesses.html",
        illnesses=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(pagination.per_page)
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/detail/<int:illness_id>", methods=["GET", "POST"])
@login_required
def detail(illness_id: int):
    form = f.IllnessForm()

    illness = db.session.get(m.Illness, illness_id)
    if not illness or illness.is_deleted:
        log(log.INFO, "Error can't find illness id:[%d]", illness_id)
        return "No Illness", 404

    if request.method == "POST" and form.validate_on_submit():
        is_name_exist = db.session.scalar(
            sa.Select(m.Illness.name).where(m.Illness.name == form.name.data, m.Illness.id != illness_id)
        )
        if is_name_exist:
            log(log.INFO, "Illness name already exist! [%s]", form.name.data)
            flash("Illness name already exist!", "danger")
            return redirect(url_for("illness.get_all"))

        illness.name = form.name.data
        illness.reason = form.reason.data
        illness.symptoms = form.symptoms.data
        illness.treatment = form.treatment.data
        log(log.INFO, "Illness updated! [%s]", illness)
        flash("Illness updated!", "success")
        illness.save()
        return redirect(url_for("illness.get_all"))
    if form.errors:
        log(log.INFO, "Form error Illness! [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        return redirect(url_for("illness.get_all"))

    form.name.data = illness.name
    form.reason.data = illness.reason
    form.symptoms.data = illness.symptoms
    form.treatment.data = illness.treatment

    return render_template("illness/modal_form.html", form=form, illness_id=illness_id)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = f.IllnessForm()

    if request.method == "POST" and form.validate_on_submit():
        is_name_exist = db.session.scalar(sa.Select(m.Illness.name).where(m.Illness.name == form.name.data))

        if is_name_exist:
            flash("Illness name already exist!", "danger")
            return redirect(url_for("illness.get_all"))

        illness = m.Illness(
            name=form.name.data,
            reason=form.reason.data,
            symptoms=form.symptoms.data,
            treatment=form.treatment.data,
            # TODO photos=form.photos.data,
        )
        log(log.INFO, "Form submitted. Illness: [%s]", illness)
        flash("Illness added!", "success")
        illness.save()
        return redirect(url_for("illness.get_all"))
    if form.errors:
        flash("Error with creating new Illness", "danger")
        return redirect(url_for("illness.get_all"))

    return render_template("illness/modal_form.html", form=form, illness_id=None)


@bp.route("/delete/<int:illness_id>", methods=["GET", "DELETE"])
@login_required
def delete(illness_id: int):
    illness = db.session.get(m.Illness, illness_id)
    if not illness or illness.is_deleted:
        log(log.INFO, "Error can't find illness id:[%d]", illness_id)
        return "No Illness", 404

    if request.method == "DELETE":
        illness.is_deleted = True
        illness.name = f"{illness.name}-deleted_at: {datetime.now()}"
        illness.plant_families = []
        illness.plant_varieties = []
        db.session.commit()
        log(log.INFO, "Illness deleted. id: [%d]", illness_id)
        return "success", 200

    return render_template("illness/confirm_delete.html", illness_id=illness_id)
