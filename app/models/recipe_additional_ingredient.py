from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin, generate_uuid


if TYPE_CHECKING:
    from .additional_ingredient import AdditionalIngredient
    from .recipe import Recipe


class RecipeAdditionalIngredient(db.Model, ModelMixin):
    __tablename__ = "recipe_additional_ingredients"

    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), default=generate_uuid, index=True)
    recipe_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("recipes.id"), primary_key=True)
    additional_ingredient_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("additional_ingredients.id"), primary_key=True
    )
    text_quantity: orm.Mapped[str] = orm.mapped_column(sa.String(64))

    additional_ingredient: orm.Mapped["AdditionalIngredient"] = orm.relationship()
    recipe: orm.Mapped["Recipe"] = orm.relationship(back_populates="additional_ingredients")

    @property
    def name(self):
        return self.additional_ingredient.name

    def __repr__(self):
        return f"<RecipeAdditionalIngredient: {self.name}>"
