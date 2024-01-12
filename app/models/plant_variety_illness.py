import sqlalchemy as sa


from app.database import db


plant_variety_illness = sa.Table(
    "plant_variety_illnesses",
    db.Model.metadata,
    sa.Column("plant_variety_id", sa.ForeignKey("plant_varieties.id"), primary_key=True),
    sa.Column("illness_id", sa.ForeignKey("illnesses.id"), primary_key=True),
)
