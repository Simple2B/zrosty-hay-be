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
    query = m.Illness.select().order_by(m.Illness.id)
    count_query = sa.select(sa.func.count()).select_from(m.Illness)
    if q:
        query = (
            m.Illness.select()
            .where(m.Illness.name.ilike(f"%{q}%"))
            .order_by(m.Illness.id)
        )
        count_query = (
            sa.select(sa.func.count())
            .where(m.Illness.name.ilike(f"%{q}%"))
            .select_from(m.Illness)
        )

    pagination = create_pagination(total=db.session.scalar(count_query))

    return render_template(
        "illness/illnesses.html",
        illnesses=db.session.execute(
            query.offset((pagination.page - 1) * pagination.per_page).limit(
                pagination.per_page
            )
        ).scalars(),
        page=pagination,
        search_query=q,
    )


@bp.route("/detail/<int:illness_id>", methods=["GET", "POST"])
@login_required
def detail(illness_id: int):
    form = f.IllnessForm()

    illness = db.session.get(m.Illness, illness_id)
    if not illness:
        log(log.INFO, "Error can't find illness id:[%d]", illness_id)
        return "No Illness", 404
    if request.method == "POST":
        if form.validate_on_submit():
            illness.name = form.name.data
            illness.reason = form.reason.data
            illness.symptoms = form.symptoms.data
            illness.treatment = form.treatment.data
            log(log.INFO, "Illness updated! [%s]", illness)
            flash("Illness updated!", "success")
            illness.save()
        if form.errors:
            log(log.INFO, "Form error Illness! [%s]", form.errors)
            flash(f"{form.errors}", "danger")
        return redirect(url_for("illness.get_all"))

    return render_template("illness/edit.html", form=form, illness=illness)


@bp.route("/create", methods=["POST"])
@login_required
def create():
    form = f.IllnessForm()
    if form.validate_on_submit():
        illness = m.Illness(
            name=form.name.data,
            reason=form.reason.data,
            symptoms=form.symptoms.data,
            treatment=form.treatment.data,
            # photos=form.photos.data,
        )
        log(log.INFO, "Form submitted. Illness: [%s]", illness)
        flash("Illness added!", "success")
        illness.save()
    else:
        flash("Error with creating new Illness", "danger")

    return redirect(url_for("illness.get_all"))


@bp.route("/delete/<int:illness_id>", methods=["GET", "DELETE"])
@login_required
def delete(illness_id: int):
    illness = db.session.get(m.Illness, illness_id)
    if not illness:
        log(log.INFO, "Error can't find illness id:[%d]", illness_id)
        return "No Illness", 404

    if request.method == "DELETE":
        db.session.delete(illness)
        db.session.commit()
        log(log.INFO, "Illness deleted. id: [%d]", illness_id)
        return "success", 200

    return render_template("illness/confirm_delete.html", illness_id=illness_id)
