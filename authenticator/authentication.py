from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
import jwt

from authenticator.models import TokenBlackList

class Authentication(BaseAuthentication):
  def authenticate(self, request):
    try:
      users = User.objects
      auth_header = request.headers.get("Authorization")
      if not auth_header:
        return None
      access_token = auth_header.split(' ')[1]
      decoded_payload = jwt.decode(access_token, 
                                  'thisisakey', 
                                  algorithms="HS256")
      uid = decoded_payload["uid"]
      jti = decoded_payload["jti"]
      user = users.filter(id=uid).first()
      if TokenBlackList.objects.filter(id=jti).first():
        raise ValidationError(
          'Incorrect authentication credentials.') #fix this later
      if user:
        request.jti = jti
        request.uid = uid
        return (user, None)
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed({'message': 'Token expired'})
    except jwt.exceptions.PyJWTError:
      raise ValidationError({'message': 'Token validation error'})
    return None