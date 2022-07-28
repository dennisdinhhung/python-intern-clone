import jwt

def token_generator(user):
    payload = {
        "uid": user.id,
        "username": user.username
    }
    key = 'thisisakey'
    token = jwt.encode(payload, key)
    return token