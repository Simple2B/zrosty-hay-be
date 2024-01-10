import sqlalchemy as sa


from app.database import db


pest_photo = sa.Table(
    "pest_photos",
    db.Model.metadata,
    sa.Column("pest_id", sa.ForeignKey("pests.id"), primary_key=True),
    sa.Column("photo_id", sa.ForeignKey("photos.id"), primary_key=True),
)
