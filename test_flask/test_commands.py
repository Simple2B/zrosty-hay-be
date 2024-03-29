import sqlalchemy as sa
from flask_login.test_client import FlaskClient
from app.commands.parse_excel import parse_excel
from app.commands.parse_json import parse_json
from app.database import db
import app.models as m

xlsx_file_path = "plants_data.xlsx"
json_file_path = "plants.json"


def test_parse_excel(client: FlaskClient):
    count_of_plants = db.session.execute(sa.select(sa.func.count(m.PlantVariety.id))).scalar()
    parse_excel(xlsx_file_path, db)
    new_count = db.session.execute(sa.select(sa.func.count(m.PlantVariety.id))).scalar()
    assert new_count > count_of_plants

    # test_add_plants
    parse_json(json_file_path, db)
    count_of_plants = new_count
    new_count = db.session.execute(sa.select(sa.func.count(m.PlantVariety.id))).scalar()
    assert new_count > count_of_plants

    program_counts = db.session.execute(sa.select(sa.func.count(m.PlantingProgram.id))).scalar()
    assert program_counts > 0
