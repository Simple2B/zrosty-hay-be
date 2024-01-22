import sqlalchemy as sa
from sqlalchemy.orm import Session


from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

import app.models as m
import app.schema as s
from app.logger import log
from api.dependency import get_db


plant_router = APIRouter(prefix="/plants", tags=["Plants"])


@plant_router.get("/", status_code=status.HTTP_200_OK, response_model=Page[s.Plant])
def get_all(db: Session = Depends(get_db)):
    """Returns the plants"""
    log(log.INFO, "Get plants")

    return paginate(db, sa.select(m.PlantVariety).order_by(m.PlantVariety.created_at))


@plant_router.get(
    "/{uuid}", status_code=status.HTTP_200_OK, response_model=s.PlantDetail, responses={404: {"model": s.ApiError404}}
)
def get(uuid: str, db: Session = Depends(get_db)):
    """Returns the plants"""
    log(log.INFO, "Get plant uuid[%s]", uuid)

    plant = db.scalar(sa.select(m.PlantVariety).where(m.PlantVariety.uuid == uuid))
    if not plant or plant.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found",
        )

    return plant
