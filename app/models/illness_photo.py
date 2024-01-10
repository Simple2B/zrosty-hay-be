import sqlalchemy as sa


from app.database import db


illness_photo = sa.Table(
    "illness_photos",
    db.Model.metadata,
    sa.Column("illness_id", sa.ForeignKey("illnesses.id"), primary_key=True),
    sa.Column("photo_id", sa.ForeignKey("photos.id"), primary_key=True),
)
