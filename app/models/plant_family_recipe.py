import sqlalchemy as sa


from app.database import db


plant_family_recipe = sa.Table(
    "plant_family_recipes",
    db.Model.metadata,
    sa.Column("recipe_id", sa.ForeignKey("recipes.id"), primary_key=True),
    sa.Column("plant_family_id", sa.ForeignKey("plant_families.id"), primary_key=True),
)
