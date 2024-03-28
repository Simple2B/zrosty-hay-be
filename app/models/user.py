from typing import Self
from datetime import datetime
from uuid import uuid4

from flask_login import UserMixin, AnonymousUserMixin
import sqlalchemy as sa
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db
from .utils import ModelMixin
from app.logger import log
from app.constants import UserRole
from app import schema as s


def gen_password_reset_id() -> str:
    return str(uuid4())


class User(db.Model, UserMixin, ModelMixin):
    __tablename__ = "users"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    location_id: orm.Mapped[int | None] = orm.mapped_column(sa.ForeignKey("locations.id"))
    username: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)
    email: orm.Mapped[str] = orm.mapped_column(sa.String(128), unique=True, index=True)
    password_hash: orm.Mapped[str] = orm.mapped_column(sa.String(256), default="")
    activated: orm.Mapped[bool] = orm.mapped_column(default=False)
    google_id: orm.Mapped[str] = orm.mapped_column(sa.String(256), default="")
    apple_id: orm.Mapped[str] = orm.mapped_column(sa.String(256), default="")
    picture_url: orm.Mapped[str | None] = orm.mapped_column(sa.String(512), default=None)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.utcnow,
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=gen_password_reset_id,
    )
    reset_password_uid: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        default=gen_password_reset_id,
    )
    is_deleted: orm.Mapped[bool] = orm.mapped_column(default=False)
    role: orm.Mapped[str] = orm.mapped_column(sa.String(32), default=UserRole.user.value)
    alias: orm.Mapped[str] = orm.mapped_column(sa.String(64), default="")

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(
        cls,
        user_id,
        password,
        session: orm.Session | None = None,
    ) -> Self | None:
        if not session:
            session = db.session
        query = cls.select().where(
            (sa.func.lower(cls.username) == sa.func.lower(user_id))
            | (sa.func.lower(cls.email) == sa.func.lower(user_id))
        )
        assert session
        user = session.scalar(query)
        if not user:
            log(log.WARNING, "user:[%s] not found", user_id)
        elif check_password_hash(user.password, password):
            return user
        return None

    def reset_password(self):
        self.password_hash = ""
        self.reset_password_uid = gen_password_reset_id()
        self.save()

    def __repr__(self):
        return f"<{self.id}: {self.username},{self.email}>"

    @property
    def display_name(self):
        return self.alias or self.username

    @property
    def json(self):
        u = s.User.model_validate(self)
        return u.model_dump_json()


class AnonymousUser(AnonymousUserMixin):
    pass
