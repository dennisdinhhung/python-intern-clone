from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
import jwt

from authenticator.models import TokenBlackList

class Authentication(BaseAuthentication):
  def authenticate(self, request):
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
      return None #fix this later
    if user:
      request.jti = jti
      request.uid = uid
      return (user, None)
    return None