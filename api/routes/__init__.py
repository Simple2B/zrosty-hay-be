# flake8: noqa F401
from fastapi import APIRouter, Request

from .user import user_router
from .plant import plant_router
from .auth import router as auth_router
from .planting_step_type import router as planting_step_type_router
from .o_auth import router as o_auth_router


router = APIRouter(prefix="/api", tags=["API"])

router.include_router(user_router)
router.include_router(auth_router)
router.include_router(plant_router)
router.include_router(planting_step_type_router)
router.include_router(o_auth_router)


@router.get("/list-endpoints/")
def list_endpoints(request: Request):
    url_list = [{"path": route.path, "name": route.name} for route in request.app.routes]
    return url_list
