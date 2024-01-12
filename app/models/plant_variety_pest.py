import sqlalchemy as sa


from app.database import db


plant_variety_pest = sa.Table(
    "plant_variety_pests",
    db.Model.metadata,
    sa.Column("plant_variety_id", sa.ForeignKey("plant_varieties.id"), primary_key=True),
    sa.Column("pest_id", sa.ForeignKey("pests.id"), primary_key=True),
)
