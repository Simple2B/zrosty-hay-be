from pydantic import BaseModel, ConfigDict, Field


class PlantingStepType(BaseModel):
    uuid: str
    svg_icon: str = Field(..., alias="svgIcon")
    name: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
