import sqlalchemy as sa


from app.database import db


plant_family_plant = sa.Table(
    "plant_family_plant_varieties",
    db.Model.metadata,
    sa.Column("plant_variety_id", sa.ForeignKey("plant_varieties.id"), primary_key=True),
    sa.Column("plant_family_id", sa.ForeignKey("plant_families.id"), primary_key=True),
)
