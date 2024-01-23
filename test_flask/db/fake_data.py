from pydantic import BaseModel, ConfigDict
from app import models as m


class FakeData(BaseModel):
    plant_families: list[m.PlantFamily]
    plant_varieties: list[m.PlantVariety]
    planting_step_types: list[m.PlantingStepType]

    model_config = ConfigDict(arbitrary_types_allowed=True)
