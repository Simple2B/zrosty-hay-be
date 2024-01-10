import sqlalchemy as sa


from app.database import db


plant_family_pest = sa.Table(
    "plant_family_pests",
    db.Model.metadata,
    sa.Column("plant_family_id", sa.ForeignKey("plant_families.id"), primary_key=True),
    sa.Column("pest_id", sa.ForeignKey("pests.id"), primary_key=True),
)
