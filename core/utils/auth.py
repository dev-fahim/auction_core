from datetime import timedelta, datetime

from django.utils.timezone import now
from django.conf import settings

import jwt
from ninja import Schema


class JwtDataSchema(Schema):
    sub: str
    issuer: str
    exp: datetime


ALGORITHM = 'HS256'
SECRET = settings.SECRET_KEY


def generate_token(sub: str) -> str:
    data = JwtDataSchema(
        sub=sub,
        issuer='https://www.marvelous-tech.com',
        exp=now().utcnow() + timedelta(days=120)
    )

    return jwt.encode(payload=dict(data), key=SECRET, algorithm=ALGORITHM)


def decode_token(token: str) -> JwtDataSchema | None:
    secret = settings.SECRET_KEY
    try:
        return JwtDataSchema(**jwt.decode(jwt=token, key=secret, algorithms=ALGORITHM))
    except jwt.PyJWTError:
        return None
