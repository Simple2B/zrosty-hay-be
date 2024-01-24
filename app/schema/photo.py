from pydantic import BaseModel, Field, ConfigDict


class Photo(BaseModel):
    url_path: str = Field(alias="urlPath")
    original_name: str | None = Field(alias="originalName")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
