from pydantic import BaseModel, ConfigDict, Field

import app.models as m
from .photo import Photo


class BasePlant(BaseModel):
    uuid: str
    name: str
    is_sun_loving: bool = Field(alias="isSunLoving")
    min_size: float = Field(alias="minSize")
    max_size: float = Field(alias="maxSize")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, use_enum_values=True)


class Plant(BasePlant):
    photo: Photo | None
    min_temperature: float | None = Field(alias="minTemperature")
    max_temperature: float | None = Field(alias="maxTemperature")
    care_type: m.CareType = Field(alias="careType")
    watering: m.CareType


class PlantDetail(BasePlant):
    features: str
    general_info: str = Field(alias="generalInfo")
    temperature_info: str = Field(alias="temperatureInfo")
    watering_info: str = Field(alias="wateringInfo")
    water_volume: float = Field(alias="waterVolume")
    humidity_percentage: float = Field(alias="humidityPercentage")

    # photos: list[Photo]


class PlantCategory(BaseModel):
    uuid: str
    name: str
    svg_icon: str = Field(alias="svgIcon")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
