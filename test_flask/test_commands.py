from flask_login.test_client import FlaskClient
from app.commands.parse_excel import parse_excel
from app.database import db

file_path = "plants_data.xlsx"


def test_parse_excel(client: FlaskClient):
    assert parse_excel(file_path, db) is None
