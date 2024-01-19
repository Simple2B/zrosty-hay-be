from pydantic import BaseModel


class S3Photo(BaseModel):
    uuid: str
    url_path: str
