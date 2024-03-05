from pydantic import BaseModel
from .planting_step_type import PlantingStepType


class TestUser(BaseModel):
    __test__ = False

    username: str
    email: str
    password: str


class TestPlantFamily(BaseModel):
    __test__ = False

    name: str
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
    humidity_percentage: float = 0
    water_volume: float = 0
    care_type: str
    is_moisture_loving: bool = False
    is_sun_loving: bool = True
    ground_ph: float = 0
    ground_type: str = ""
    can_plant_indoors: bool = False


class TestPlantVarietyAndProgram(TestPlantVariety):
    __test__ = False
    harvest_time: int = 0
    planting_time: int = 0


class TestPlantCategory(BaseModel):
    __test__ = False

    name: str
    svg_icon: str


class TestStepType(PlantingStepType):
    __test__ = False


class TestRecipe(BaseModel):
    __test__ = False

    name: str
    description: str
    cooking_time: int
    additional_ingredients: str


class TestRecipeCategory(BaseModel):
    __test__ = False

    name: str


class TestData(BaseModel):
    __test__ = False

    test_users: list[TestUser]

    categories: list[TestPlantCategory]
    plant_families: list[TestPlantFamily]
    plant_varieties: list[TestPlantVariety]
    planting_step_types: list[TestStepType]
    recipes: list[TestRecipe]
    recipe_categories: list[TestRecipeCategory]
