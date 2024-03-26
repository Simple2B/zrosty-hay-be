from datetime import datetime
from uuid import uuid4

from sqlalchemy import orm
from app.database import db


class ModelMixin(object):
    def save(self, commit=True):
        # Save this model to the database.
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def as_deleted(self, commit=True):
        self.is_deleted: orm.Mapped[bool] = True
        if hasattr(self, "name"):
            self.name: orm.Mapped[str] = f"deleted_{self.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.save(commit=commit)


# Add your own utility classes and functions here.
def generate_uuid() -> str:
    return str(uuid4())
