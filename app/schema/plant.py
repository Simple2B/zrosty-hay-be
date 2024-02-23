from pydantic import BaseModel, ConfigDict, Field

import app.models as m
from .photo import Photo


class InstanceName(BaseModel):
    uuid: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class BasePlant(BaseModel):
    uuid: str
    name: str
    care_type: m.CareType = Field(alias="careType")
    is_sun_loving: bool = Field(alias="isSunLoving")
    min_size: float = Field(alias="minSize")
    max_size: float = Field(alias="maxSize")
    watering: m.CareType

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, use_enum_values=True)


class Plant(BasePlant):
    photo: Photo | None
    min_temperature: float | None = Field(alias="minTemperature")
    max_temperature: float | None = Field(alias="maxTemperature")


class PlantDetail(BasePlant):
    general_info: str = Field(alias="generalInfo")
    features: str
    humidity_percentage: float = Field(alias="humidityPercentage")
    harvest_time: int = Field(alias="harvestTime")
    planting_time: int = Field(alias="plantingTime")


class PlantCareTips(BaseModel):
    watering: m.CareType
    watering_info: str = Field(alias="wateringInfo")
    min_temperature: float | None = Field(alias="minTemperature")
    max_temperature: float | None = Field(alias="maxTemperature")
    temperature_info: str
    ground_ph: float = Field(alias="groundPh")
    ground_type: str = Field(alias="groundType")
    pests: list[InstanceName]
    illnesses: list[InstanceName]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True, use_enum_values=True)


class PlantCategory(BaseModel):
    uuid: str
    name: str
    svg_icon: str = Field(alias="svgIcon")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
