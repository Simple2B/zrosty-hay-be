from pydantic import BaseModel


class GoogleAuthTokenIn(BaseModel):
    id_token: str


class GoogleTokenVerification(BaseModel):
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    name: str
    picture: str
    given_name: str
    family_name: str
    locale: str
    iat: int
    exp: int


class AppleAuthTokenIn(BaseModel):
    id_token: str


class AppleAuthenticationFullName(BaseModel):
    givenName: str | None = None
    familyName: str | None = None


class AppleTokenVerification(BaseModel):
    iss: str
    aud: str
    exp: int
    iat: int
    sub: str
    c_hash: str
    email: str
    email_verified: bool
    auth_time: int
    nonce_supported: bool
    fullName: AppleAuthenticationFullName | None = None
