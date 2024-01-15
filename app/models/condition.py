import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin


class Condition(db.Model, ModelMixin):
    __tablename__ = "conditions"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    # Foreign keys
    plant_variety_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("plant_varieties.id"), nullable=False
    )

    # Fields
    general_info: orm.Mapped[str] = orm.mapped_column(sa.String(2048), default="", nullable=True)
    temperature_info: orm.Mapped[str] = orm.mapped_column(sa.String(2048), default="", nullable=True)
    watering_info: orm.Mapped[str] = orm.mapped_column(sa.String(2048), default="", nullable=True)
    planting_min_temperature: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=True)
    planting_max_temperature: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=True)
    is_moisture_loving: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True, nullable=True)
    is_sun_loving: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False, nullable=True)
    ground_ph: orm.Mapped[int] = orm.mapped_column(sa.String(64), nullable=True)
    ground_type: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=True)
    can_plant_indoors: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False, nullable=True)

    def __repr__(self):
        return f"<Condition: {self.id}>"
