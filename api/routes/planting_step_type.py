import sqlalchemy as sa
from sqlalchemy.orm import Session


from fastapi import APIRouter, Depends, status

import app.models as m
import app.schema as s
from app.logger import log
from api.dependency import get_db


router = APIRouter(prefix="/planting-step-types", tags=["Planting Step Types"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[s.PlantingStepType])
def get_all_planting_step_types(
    db: Session = Depends(get_db),
):
    """Returns all planting step types"""
    log(log.INFO, "Get all planting step types")
    step_types = db.scalars(sa.select(m.PlantingStepType)).all()

    return step_types
