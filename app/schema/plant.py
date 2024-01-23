from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query

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

    photos: list[Photo]


class SearchPlantsQueryParams(BaseModel):
    name: str = Query("", max_length=64)
    can_plant_indoors: None | bool = Query(None)
    type_of: None | m.PlantFamilyType = Query(None)

    model_config = ConfigDict(use_enum_values=True)
