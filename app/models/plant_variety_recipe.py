import sqlalchemy as sa


from app.database import db


plant_variety_recipe = sa.Table(
    "plant_variety_recipe",
    db.Model.metadata,
    sa.Column("recipe_id", sa.ForeignKey("recipes.id"), primary_key=True),
    sa.Column("plant_variety_id", sa.ForeignKey("plant_varieties.id"), primary_key=True),
)
