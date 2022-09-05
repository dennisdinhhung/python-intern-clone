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
      
      split = auth_header.split(' ')
      if len(split) != 2:
        raise AuthenticationFailed('Token invalid')
      
      access_token = split[1]
      decoded_payload = jwt.decode(jwt = access_token, 
                                  key = settings.SECRET_KEY, 
                                  algorithms = "HS256")
      user_id = decoded_payload.get('uid')
      jti = decoded_payload.get('jti')
      if TokenBlackList.objects.filter(id=jti, user_id=user_id).exists():
        raise ValidationError('Incorrect authentication credentials.')
        
      user = users.filter(id=user_id).first()
      if user:
        request.jti = jti
        request.uid = user_id
        return (user, None)
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Token expired')
    except jwt.exceptions.PyJWTError:
      raise ValidationError('Token validation error')
    except Exception as exception:
      raise AuthenticationFailed(exception)
  
  def authenticate_header(self, request):
    return "Authentication error"