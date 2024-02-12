import sqlalchemy as sa
from sqlalchemy.orm import Session


from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

import app.models as m
import app.schema as s
from app.logger import log
from api.dependency import get_db, get_plant


plant_router = APIRouter(prefix="/plants", tags=["Plants"])


@plant_router.get("/", status_code=status.HTTP_200_OK, response_model=Page[s.Plant])
def get_all(
    name: str = Query("", max_length=64),
    category_uuids: list[str] = Query([]),
    db: Session = Depends(get_db),
):
    """Returns the plants"""
    log(log.INFO, "Get plants")
    query = sa.select(m.PlantVariety)
    if name:
        query = query.where(m.PlantVariety.name.ilike(f"%{name}%"))

    if category_uuids:
        query = query.join(m.PlantFamily).where(
            sa.or_(
                m.PlantVariety.categories.any(
                    m.PlantCategory.uuid.in_(category_uuids),
                ),
                m.PlantFamily.categories.any(m.PlantCategory.uuid.in_(category_uuids)),
            )
        )

    return paginate(db, query.order_by(m.PlantVariety.id.desc()))


@plant_router.get(
    "/categories",
    status_code=status.HTTP_200_OK,
    response_model=list[s.PlantCategory],
)
def get_categories(db: Session = Depends(get_db)):
    """Returns the plants"""
    log(log.INFO, "Get plants categories ")

    categories = db.scalars(sa.select(m.PlantCategory)).all()
    return categories


@plant_router.get(
    "/{uuid}", status_code=status.HTTP_200_OK, response_model=s.PlantDetail, responses={404: {"model": s.ApiError404}}
)
def get(uuid: str, plant: m.PlantVariety = Depends(get_plant)):
    """Returns the plants"""
    log(log.INFO, "Get plant uuid[%s]", uuid)

    return plant


@plant_router.get(
    "/{uuid}/photos",
    status_code=status.HTTP_200_OK,
    response_model=list[s.Photo],
    responses={404: {"model": s.ApiError404}},
)
def get_plant_photos(uuid: str, plant: m.PlantVariety = Depends(get_plant)):
    """Returns the plant photos"""
    log(log.INFO, "Get plant photos uuid[%s]", uuid)

    return plant.photos


@plant_router.get(
    "/{uuid}/steps",
    status_code=status.HTTP_200_OK,
    response_model=list[s.PlantingStep],
    responses={404: {"model": s.ApiError404}},
)
def get_planting_steps(uuid: str, plant: m.PlantVariety = Depends(get_plant)):
    """Returns the plant program steps"""
    log(log.INFO, "Get plant program steps uuid[%s]", uuid)

    if not plant.programs:
        log(log.INFO, "No program found for plant uuid[%s]", uuid)
        return []

    steps = {}  # type:ignore
    # currently, we only need to have one program
    for step in plant.programs[0].steps:
        day = step.day
        step_type = step.step_type
        if day in steps:
            steps[day]["step_type"].append(step_type)
        else:
            steps[day] = {"day": day, "step_type": [step_type]}

    return list(steps.values())
