import enum


class UserRole(enum.Enum):
    user = "user"
    admin = "admin"


class UserPreferredLanguage(enum.Enum):
    en = "en"
    ua = "ua"
