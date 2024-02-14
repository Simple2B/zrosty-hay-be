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
from .recipe_category import recipe_categories


if TYPE_CHECKING:
    from .plant_family import PlantFamily
    from .plant_variety import PlantVariety
    from .photo import Photo
    from .category import Category


class Recipe(db.Model, ModelMixin):
    __tablename__ = "recipes"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)

    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), default=generate_uuid, index=True)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)

    cooking_time: orm.Mapped[int] = orm.mapped_column(default=0)
    additional_ingredients: orm.Mapped[str] = orm.mapped_column(sa.String(1024), default="")
    description: orm.Mapped[str] = orm.mapped_column(sa.Text)

    # Relationships
    plant_families: orm.Mapped[List["PlantFamily"]] = orm.relationship(secondary=plant_family_recipe)
    plant_varieties: orm.Mapped[List["PlantVariety"]] = orm.relationship(secondary=plant_variety_recipe)
    categories: orm.Mapped[List["Category"]] = orm.relationship(secondary=recipe_categories)

    photos: orm.Mapped[List["Photo"]] = orm.relationship(secondary=recipe_photo)
    steps: orm.Mapped[List["RecipeStep"]] = orm.relationship(order_by="RecipeStep.step_number", back_populates="recipe")

    @property
    def photo(self):
        return self.photos[0] if self.photos else None

    def __repr__(self):
        return f"<Id: {self.id}, Recipe: {self.name}>"
