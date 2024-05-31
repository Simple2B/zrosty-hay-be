from typing import TYPE_CHECKING, Union

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin, generate_uuid


if TYPE_CHECKING:
    from .plant_family import PlantFamily
    from .plant_variety import PlantVariety


class RecipeIngredient(db.Model, ModelMixin):
    __tablename__ = "recipe_ingredients"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), default=generate_uuid, index=True)

    recipe_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("recipes.id"))
    plant_family_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("plant_families.id"))
    plant_variety_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("plant_varieties.id"))

    quantity: orm.Mapped[float] = orm.mapped_column()
    quantity_type: orm.Mapped[str] = orm.mapped_column(sa.String(64))

    plant_family: orm.Mapped["PlantFamily"] = orm.relationship()
    plant_variety: orm.Mapped[Union["PlantVariety", None]] = orm.relationship()

    @property
    def name(self):
        return self.plant_variety.name if self.plant_variety else self.plant_family.name if self.plant_family else ""

    @property
    def photo(self):
        if self.plant_variety and self.plant_variety.photo:
            return self.plant_variety.photo

        for plant in self.plant_family.plant_varieties:
            if plant.photo:
                return plant.photo

    def __repr__(self):
        return f"<Id: {self.id}, RecipeIngredient: {self.name}>"
