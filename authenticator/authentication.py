import jwt
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed

from authenticator.models import TokenBlackList


class Authentication(BaseAuthentication):
  def authenticate(self, request):
    try:
      users = User.objects
      auth_header = request.headers.get("Authorization")
      if not auth_header:
        return None
      
      access_token = auth_header.split(' ')[1] #catch if the token has 1 item 
      decoded_payload = jwt.decode(jwt = access_token, 
                                  key = settings.SECRET_KEY, 
                                  algorithms = "HS256")
      user_id = decoded_payload["uid"]
      jti = decoded_payload["jti"]
      if TokenBlackList.objects.filter(id=jti).first():
        raise ValidationError(
          'Incorrect authentication credentials.')
        
      user = users.filter(id=user_id).first()
      if user:
        request.jti = jti
        request.uid = user_id
        return (user, None)
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed({'message': 'Token expired'})
    except jwt.exceptions.PyJWTError:
      raise ValidationError({'message': 'Token validation error'})
    return None
  
  def authenticate_header(self, request): #wtf is this
    return "Authentication error"