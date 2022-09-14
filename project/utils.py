import uuid
import datetime

import jwt
from django.conf import settings


def token_generator(user_id, exp_time):
    payload = {
        "jti": uuid.uuid4().hex,
        "uid": user_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(exp_time)),
    }
    secret_key = settings.SECRET_KEY
    token = jwt.encode(payload, secret_key)
    return token
