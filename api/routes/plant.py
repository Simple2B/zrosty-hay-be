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
def get_all(query_params: s.SearchPlantsQueryParams = Depends(), db: Session = Depends(get_db)):
    """Returns the plants"""
    log(log.INFO, "Get plants")
    query = sa.select(m.PlantVariety)
    if query_params.name:
        query = query.where(m.PlantVariety.name.ilike(f"%{query_params.name}%"))
    if query_params.can_plant_indoors is not None:
        query = query.where(m.PlantVariety.can_plant_indoors.is_(query_params.can_plant_indoors))
    if query_params.type_of:
        query = query.join(m.PlantFamily).where(m.PlantFamily.type_of == query_params.type_of.value)

    return paginate(db, query)


@plant_router.get(
    "/{uuid}", status_code=status.HTTP_200_OK, response_model=s.PlantDetail, responses={404: {"model": s.ApiError404}}
)
def get(uuid: str, db: Session = Depends(get_db)):
    """Returns the plants"""
    log(log.INFO, "Get plant uuid[%s]", uuid)

    plant = db.scalar(sa.select(m.PlantVariety).where(m.PlantVariety.uuid == uuid))
    if not plant or plant.is_deleted:
        log(log.ERROR, "Not found plant: [%s]", uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plant not found",
        )

    return plant
