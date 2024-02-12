import sqlalchemy as sa
from sqlalchemy.orm import Session


from fastapi import APIRouter, Depends, status

import app.models as m
import app.schema as s
from app.logger import log
from api.dependency import get_db


router = APIRouter(prefix="/planting-step-types", tags=["PlantingStepTypes"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[s.PlantingStepType])
def get_all(
    db: Session = Depends(get_db),
):
    """Returns all step types"""
    log(log.INFO, "Get all step types")
    step_types = db.scalars(sa.select(m.PlantingStepType)).all()

    return step_types
