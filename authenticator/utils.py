import uuid
import datetime
import jwt
from django.conf import settings


def token_generator(user, exp_time):
    payload = {
        "jti": uuid.uuid4().hex,
        "uid": user.id,
        "username": user.username,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(exp_time)),
    }
    key = settings.SECRET_KEY
    token = jwt.encode(payload, key)
    return token