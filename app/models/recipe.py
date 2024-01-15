from datetime import datetime
from typing import TYPE_CHECKING, List

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin, generate_uuid
from .recipe_photo import recipe_photo
from .plant_family_recipe import plant_family_recipe
from .plant_variety_recipe import plant_variety_recipe
from .recipe_step import RecipeStep


if TYPE_CHECKING:
    from .plant_family import PlantFamily
    from .plant_variety import PlantVariety
    from .photo import Photo


class Recipe(db.Model, ModelMixin):
    __tablename__ = "recipes"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        unique=True,
        nullable=False,
    )

    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime,
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_deleted: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

    cooking_time: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, default=0, nullable=True
    )
    additional_ingredients: orm.Mapped[str] = orm.mapped_column(
        sa.String(1024), default="", nullable=True
    )

    # Relationships
    plant_families: orm.Mapped[List["PlantFamily"]] = orm.relationship(
        secondary=plant_family_recipe
    )
    plant_varieties: orm.Mapped[List["PlantVariety"]] = orm.relationship(
        secondary=plant_variety_recipe
    )
    photos: orm.Mapped[List["Photo"]] = orm.relationship(secondary=recipe_photo)
    steps: orm.Mapped[List["RecipeStep"]] = orm.relationship(
        order_by="RecipeStep.step_number", back_populates="recipe"
    )

    def __repr__(self):
        return f"<Id: {self.id}, Recipe: {self.name}>"
