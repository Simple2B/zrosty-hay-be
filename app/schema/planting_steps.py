from pydantic import BaseModel, Field, ConfigDict


class StepType(BaseModel):
    uuid: str
    color: str


class PlantingStep(BaseModel):
    day: int
    step_types: list[StepType] = Field(..., alias="stepType")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
