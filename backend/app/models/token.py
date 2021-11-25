from datetime import datetime, timedelta
from pydantic import EmailStr

from app.core.config import JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.core import CoreModel


class JWTMeta(CoreModel):
    iss: str = "stitcher.io"
    aud: str = JWT_AUDIENCE
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(
        datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

class JWTCreds(CoreModel):
    """How we'll identify users"""
    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    """JWT payload right before it's encoded"""
    pass

class AccessToken(CoreModel):
    access_token: str
    token_type: str



