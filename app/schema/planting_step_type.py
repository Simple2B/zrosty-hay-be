from pydantic import BaseModel, ConfigDict


class PlantingStepType(BaseModel):
    uuid: str
    color: str
    svg_icon: str
    name: str

    model_config = ConfigDict(from_attributes=True)
