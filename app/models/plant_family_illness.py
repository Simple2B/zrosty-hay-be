import sqlalchemy as sa


from app.database import db


plant_family_illness = sa.Table(
    "plant_family_illnesses",
    db.Model.metadata,
    sa.Column("plant_family_id", sa.ForeignKey("plant_families.id"), primary_key=True),
    sa.Column("illness_id", sa.ForeignKey("illnesses.id"), primary_key=True),
)
