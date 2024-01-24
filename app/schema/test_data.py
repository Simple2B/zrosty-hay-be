from pydantic import BaseModel


class TestUser(BaseModel):
    __test__ = False

    username: str
    email: str
    password: str


class TestPlantFamily(BaseModel):
    __test__ = False

    name: str
    type_of: str
    features: str


class TestPlantVariety(BaseModel):
    __test__ = False

    plant_family_id: int
    name: str
    features: str
    general_info: str
    temperature_info: str
    watering_info: str
    min_temperature: float
    max_temperature: float
    min_size: float
    max_size: float
    humidity_percentage: float
    water_volume: float
    care_type: str
    is_moisture_loving: bool
    is_sun_loving: bool
    ground_ph: float
    ground_type: str
    can_plant_indoors: bool


class TestData(BaseModel):
    __test__ = False

    test_users: list[TestUser]

    plant_families: list[TestPlantFamily]
    plant_varieties: list[TestPlantVariety]
