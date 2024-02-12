from pydantic import BaseModel, Field, ConfigDict


class PlantingStepType(BaseModel):
    uuid: str
    color: str


class PlantingStep(BaseModel):
    day: int
    step_type: list[PlantingStepType] = Field([], alias="stepType")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
