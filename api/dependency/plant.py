from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session
import sqlalchemy as sa

from app.database import get_db
import app.models as m
from app.logger import log


def get_plant(uuid: str, db: Session = Depends(get_db)) -> m.PlantVariety | None:
    """Raises an exception if the plant user not found"""

    log(log.INFO, "Get plant: [%s]", uuid)

    plant = db.scalar(sa.select(m.PlantVariety).where(m.PlantVariety.uuid == uuid))
    if not plant or plant.is_deleted:
        log(log.ERROR, "Not found plant: [%s]", uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found",
        )

    return plant
