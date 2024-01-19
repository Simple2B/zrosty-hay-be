from uuid import uuid4
from app.database import db


class ModelMixin(object):
    def save(self, commit=True):
        # Save this model to the database.
        db.session.add(self)
        if commit:
            db.session.commit()
        return self


# Add your own utility classes and functions here.
def generate_uuid() -> str:
    return str(uuid4())
