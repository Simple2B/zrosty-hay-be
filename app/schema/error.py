from pydantic import BaseModel


class ApiError404(BaseModel):
    detail: str
