from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import db


# TODO not finish
class DBPopulator:
    DB_MODEL: db.Model
    SCHEMA_MODEL: BaseModel
    DATA_FAKE_MAP: dict

    def __init__(self) -> None:
        model_fields = self.SCHEMA_MODEL.model_fields.keys()
        for field in self.DATA_FAKE_MAP:
            if field not in model_fields:
                raise KeyError(f"Filed: {field} not in model_fields: {self.SCHEMA_MODEL}")

    def create_fake_data(self):
        fake_data = dict()
        for field, data_generator in self.DATA_FAKE_MAP.items():
            fake_data[field] = data_generator()
        return self.SCHEMA_MODEL.model_validate(fake_data)

    def create(self, data: dict, session: Session):
        model_data = self.SCHEMA_MODEL.model_validate(data)
        model_db = self.DB_MODEL(**model_data.model_dump(exclude_none=True))
        session.add(model_db)
        return model_db
