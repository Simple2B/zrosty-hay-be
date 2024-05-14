import json
from flask import (
    Blueprint,
    render_template,

)
from flask_login import login_required
from sqlalchemy import func, extract
import calendar

from app import models as m, db


bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@bp.route("/", methods=["GET"])
@login_required
def get_all():

    plant_categories = db.session.query(m.PlantCategory).all()
    plant_categories_data = [{'name': category.name, 'amount': len(category.plant_families)} for category in plant_categories]
    plant_categories_data_json = json.dumps(plant_categories_data)

    plant_variety_counts = (
        db.session.query(
            extract('year', m.PlantVariety.created_at),
            extract('month', m.PlantVariety.created_at),
            func.count(m.PlantVariety.id)
        )
        .group_by(
            extract('year', m.PlantVariety.created_at),
            extract('month', m.PlantVariety.created_at)
        )
        .all()
    )

    plant_variety_data = [{'date': f'{calendar.month_abbr[month]} {int(year)}', 'amount': count} for year, month, count in plant_variety_counts]
    plant_variety_data_json = json.dumps(plant_variety_data)

    plant_variety_count = db.session.query(func.count(m.PlantVariety.id)).scalar()
    plant_families_count = db.session.query(func.count(m.PlantFamily.id)).scalar()
    user_count = db.session.query(func.count(m.User.id)).scalar()
    recipe_count = db.session.query(func.count(m.Recipe.id)).scalar()
    pest_count = db.session.query(func.count(m.Pest.id)).scalar()


    return render_template(
        "dashboard/dashboard.html",
        plant_categories_data_json=plant_categories_data_json,
        plant_variety_data_json=plant_variety_data_json,
        plant_variety_count=plant_variety_count,
        plant_families_count=plant_families_count,
        user_count=user_count,
        recipe_count=recipe_count,
        pest_count=pest_count,
    )

