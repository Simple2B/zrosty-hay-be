import sqlalchemy as sa


from app.database import db


plant_family_category = sa.Table(
    "plant_family_categories",
    db.Model.metadata,
    sa.Column("plant_family_id", sa.ForeignKey("plant_families.id"), primary_key=True),
    sa.Column("plant_category_id", sa.ForeignKey("plant_categories.id"), primary_key=True),
)
