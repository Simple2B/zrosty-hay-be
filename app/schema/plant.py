from pydantic import BaseModel, ConfigDict, Field

import app.models as m


class Plant(BaseModel):
    uuid: str
    is_sun_loving: bool = Field(alias="isSunLoving")
    temperature: str
    size: str
    care_type: m.CareType = Field(alias="careType")
    watering: m.CareType

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, use_enum_values=True)


class PlantDetail(BaseModel):
    features: str
    general_info: str = Field(alias="generalInfo")
    temperature_info: str = Field(alias="temperatureInfo")
    watering_info: str = Field(alias="wateringInfo")
    water_volume: float = Field(alias="waterVolume")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
