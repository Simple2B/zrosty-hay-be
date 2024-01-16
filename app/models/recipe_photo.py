import sqlalchemy as sa


from app.database import db


recipe_photo = sa.Table(
    "recipe_photos",
    db.Model.metadata,
    sa.Column("recipe_id", sa.ForeignKey("recipes.id"), primary_key=True),
    sa.Column("photo_id", sa.ForeignKey("photos.id"), primary_key=True),
)
