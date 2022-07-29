import jwt
import uuid


def token_generator(user):
    payload = {
        "jti": uuid.uuid4().hex,
        "uid": user.id,
        "username": user.username
    }
    key = 'thisisakey'
    token = jwt.encode(payload, key)
    return token