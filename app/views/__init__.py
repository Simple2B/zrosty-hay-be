# ruff: noqa: F401
from .auth import auth_blueprint
from .main import main_blueprint
from .user import bp as user_blueprint
from .pest import bp as pest_blueprint
from .illness import bp as illness_blueprint
from .plant_family import bp as plant_family_blueprint
from .plant_variety import bp as plant_varieties_blueprint
from .photo import bp as photos_blueprint
from .planting_program import bp as planting_program_blueprint
from .planting_step_type import bp as planting_step_type_blueprint
from .plant_category import bp as plant_category_blueprint
from .program_step import bp as program_step_blueprint
from .category import bp as category_blueprint
