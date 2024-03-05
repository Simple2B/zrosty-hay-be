import os

import sqlalchemy as sa
import pandas as pd
import app.models as m

care_type = {
    "легкий": m.CareType.easy.value,
    "середній": m.CareType.normal.value,
    "складний": m.CareType.hard.value,
}


def parse_excel(fail_path: str, db):
    if not os.path.isfile(fail_path):
        print(f"File not exist in {fail_path}")
        return
    plant_sheet = pd.read_excel(fail_path)

    print("Set new plant category and family")
    for index, row in plant_sheet.iterrows():
        plant_data = list(row.values)
        plant_category_name = plant_data[0]
        plant_family_name = plant_data[1]
        if pd.isna(plant_family_name):
            print("Can't find family")
            continue
        family = db.session.scalar(
            sa.select(m.PlantFamily).where(sa.func.lower(m.PlantFamily.name) == sa.func.lower(plant_family_name))
        )
        if not family:
            family = m.PlantFamily(name=plant_family_name)
            db.session.add(family)
            db.session.flush()
        if pd.isna(plant_category_name):
            print("Can't find category")
            continue
        category = db.session.scalar(
            sa.select(m.PlantCategory).where(sa.func.lower(m.PlantCategory.name) == sa.func.lower(plant_category_name))
        )
        if not category:
            category = m.PlantCategory(name=plant_category_name, svg_icon="")
            db.session.add(category)
            db.session.flush()
            family.categories.append(category)
        db.session.commit()

    for index, row in plant_sheet.iterrows():
        print(f"Row {index + 1}:")
        plant_data = list(row.values)
        plant_category_name = plant_data[0]
        if pd.isna(plant_category_name):
            continue
        plant_family_name = plant_data[1]
        family = db.session.scalar(
            sa.select(m.PlantFamily).where(sa.func.lower(m.PlantFamily.name) == sa.func.lower(plant_family_name))
        )
        if not family:
            print("Can't find family")
            return
        temperature = (
            [15, 25]
            if pd.isna(plant_data[12])
            else [int(tem) for tem in str(plant_data[12]).split(".") if tem.isdigit()]
        )
        try:
            min_temperature = temperature[0]
        except IndexError:
            min_temperature = 15
        try:
            max_temperature = temperature[1]
        except IndexError:
            max_temperature = 25

        plant = db.session.scalar(
            sa.select(m.PlantVariety).where(sa.func.lower(m.PlantVariety.name) == sa.func.lower(plant_data[2]))
        )
        if plant:
            print(f"Plant {plant_data[2]} already exist")
            continue

        plant = m.PlantVariety(
            family=family,
            name=plant_data[2],
            general_info=plant_data[3],
            features=plant_data[4],
            temperature_info="" if pd.isna(plant_data[5]) else plant_data[5],
            watering_info="" if pd.isna(plant_data[6]) else plant_data[6],
            humidity_percentage=60 if pd.isna(plant_data[9]) else plant_data[9],
            water_volume=500 if pd.isna(plant_data[7]) else plant_data[7],
            care_type=m.CareType.normal.value if pd.isna(plant_data[8]) else care_type[plant_data[8]],
            min_size=0 if pd.isna(plant_data[10]) else plant_data[10],
            max_size=0 if pd.isna(plant_data[11]) else plant_data[11],
            is_moisture_loving=plant_data[13],
            is_sun_loving=plant_data[14],
            can_plant_indoors=plant_data[15],
            min_temperature=min_temperature,
            max_temperature=max_temperature,
            ground_ph=0,
            ground_type="" if pd.isna(plant_data[16]) else plant_data[16],
        )

        db.session.add(plant)
    db.session.commit()
