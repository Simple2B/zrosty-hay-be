from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session
import sqlalchemy as sa

from app.database import get_db
import app.models as m
from app.logger import log


def get_recipe(uuid: str, db: Session = Depends(get_db)) -> m.PlantVariety:
    """Raises an exception if the plant user not found"""

    log(log.INFO, "Get recipe: [%s]", uuid)

    recipe = db.scalar(sa.select(m.Recipe).where(m.Recipe.uuid == uuid))
    if not recipe or recipe.is_deleted:
        log(log.ERROR, "Not found plant: [%s]", uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found",
        )

    return recipe
