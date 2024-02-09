from pydantic import BaseModel


class PlantingStep(BaseModel):
    day: int
    colors: list[str]
