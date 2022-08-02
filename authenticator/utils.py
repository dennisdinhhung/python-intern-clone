import jwt
import uuid
import datetime

def token_generator(user):
    payload = {
        "jti": uuid.uuid4().hex,
        "uid": user.id,
        "username": user.username,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
    }
    key = 'thisisakey'
    token = jwt.encode(payload, key)
    return token