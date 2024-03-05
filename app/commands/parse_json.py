from typing import List

import sqlalchemy as sa
from pydantic import TypeAdapter
from app import models as m
from app import schema as s


def parse_json(fail_path: str, db):
    """Add plants from excel file to DB."""
    print("Start")
    with open(fail_path, "r") as f:
        plants = TypeAdapter(List[s.TestPlant]).validate_json(f.read())
    # TODO not fihished
