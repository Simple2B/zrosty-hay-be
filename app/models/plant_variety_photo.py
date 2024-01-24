import sqlalchemy as sa


from app.database import db


plant_variety_photo = sa.Table(
    "plant_variety_photos",
    db.Model.metadata,
    sa.Column("plant_variety_id", sa.ForeignKey("plant_varieties.id"), primary_key=True),
    sa.Column("photo_id", sa.ForeignKey("photos.id"), primary_key=True),
)
