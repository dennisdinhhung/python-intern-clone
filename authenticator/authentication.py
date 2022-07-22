from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
import jwt

class Authentication(BaseAuthentication):
  def authenticate(self, request):
    users = User.objects
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
      return None

    access_token = auth_header.split(' ')[1]
    decoded_payload = jwt.decode(access_token, 
                                 'thisisakey', algorithms="HS256")
    uid = decoded_payload["uid"]
    user = users.filter(id=uid).first()
    
    if user:
      return (user, None)
    
    return None