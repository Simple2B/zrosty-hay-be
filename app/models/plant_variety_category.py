import sqlalchemy as sa


from app.database import db


plant_variety_category = sa.Table(
    "plant_variety_categories",
    db.Model.metadata,
    sa.Column("plant_category_id", sa.ForeignKey("plant_categories.id"), primary_key=True),
    sa.Column("plant_variety_id", sa.ForeignKey("plant_varieties.id"), primary_key=True),
)
