from typing import TYPE_CHECKING, Union

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin


if TYPE_CHECKING:
    from .plant_family import PlantFamily
    from .plant_variety import PlantVariety


class RecipeIngredient(db.Model, ModelMixin):
    __tablename__ = "recipe_ingredients"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    recipe_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("recipes.id"), primary_key=True)
    plant_familie_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("plant_families.id"))
    plant_varietie_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("plant_varieties.id"))

    quantity: orm.Mapped[float] = orm.mapped_column()
    quantity_type: orm.Mapped[str] = orm.mapped_column(sa.String(64))

    plant_varietie: orm.Mapped[Union["PlantVariety", None]] = orm.relationship()
    plant_familie: orm.Mapped[Union["PlantFamily", None]] = orm.relationship()

    def __repr__(self):
        return f"<Id: {self.id}, RecipeIngredient: {self.name}>"
