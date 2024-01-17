from pydantic import BaseModel, ConfigDict


class Pest(BaseModel):
    id: int
    name: str
    symptoms: str
    treatment: str

    model_config = ConfigDict(
        from_attributes=True,
    )
