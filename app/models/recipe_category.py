import sqlalchemy as sa


from app.database import db


recipe_categories = sa.Table(
    "recipe_categories",
    db.Model.metadata,
    sa.Column("recipe_id", sa.ForeignKey("categories.id"), primary_key=True),
    sa.Column("category_id", sa.ForeignKey("recipes.id"), primary_key=True),
)
