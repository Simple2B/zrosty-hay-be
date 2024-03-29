from pydantic import BaseModel, Field, ConfigDict


class StepType(BaseModel):
    uuid: str
    color: str


class PlantingStepDay(BaseModel):
    uuid: str
    name: str
    svg_icon: str = Field(..., alias="svgIcon")
    instruction: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PlantingStep(BaseModel):
    day: int
    step_types: list[StepType] = Field(..., alias="stepTypes")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
