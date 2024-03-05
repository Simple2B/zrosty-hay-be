from typing import List

import sqlalchemy as sa
from pydantic import TypeAdapter
from app import models as m
from app import schema as s


def parse_json(fail_path: str, db):
    """Add plants from json file to DB. Use it only for staging db"""
    print("Start")
    with open(fail_path, "r") as f:
        plants = TypeAdapter(List[s.TestPlantVarietyAndProgram]).validate_json(f.read())
    for plant in plants:
        if db.session.get(m.PlantFamily, plant.plant_family_id) is None:
            print(f"Plant family with id {plant.plant_family_id} does not exist")
            continue

        if (
            db.session.scalar(
                sa.select(m.PlantVariety).where(sa.func.lower(m.PlantVariety.name) == sa.func.lower(plant.name))
            )
            is not None
        ):
            print(f"Plant {plant.name} already exists")
            continue
        new_plant = m.PlantVariety(**plant.model_dump(exclude={"planting_time", "harvest_time"}))
        db.session.add(new_plant)
        if plant.planting_time and plant.harvest_time:
            new_plant_program = m.PlantingProgram(
                planting_time=plant.planting_time, harvest_time=plant.harvest_time, plant_variety=new_plant
            )
            db.session.add(new_plant_program)
    db.session.commit()
