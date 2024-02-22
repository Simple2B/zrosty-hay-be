import sqlalchemy as sa
from flask_login.test_client import FlaskClient
from app.commands.parse_excel import parse_excel
from app.database import db
import app.models as m

file_path = "plants_data.xlsx"


def test_parse_excel(client: FlaskClient):
    count_of_plants = db.session.execute(sa.select(sa.func.count(m.PlantVariety.id))).scalar()
    parse_excel(file_path, db)
    new_count = db.session.execute(sa.select(sa.func.count(m.PlantVariety.id))).scalar()
    assert new_count > count_of_plants
