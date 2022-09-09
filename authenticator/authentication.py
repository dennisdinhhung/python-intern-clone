import jwt
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed

from authenticator.models import TokenBlackList


class Authentication(BaseAuthentication):

    def authenticate_header(self, request):
        return "Authentication header"

    def authenticate(self, request):
        try:
            users = User.objects
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return None
            split = auth_header.split(' ')
            if len(split) != 2:
                raise AuthenticationFailed('Token invalid.')

            access_token = split[1]
            payload = jwt.decode(jwt=access_token, key=settings.SECRET_KEY, algorithms="HS256")
            jti = payload.get('jti')
            if TokenBlackList.objects.filter(id=jti).exists():
                raise ValidationError('Incorrect authentication credentials.')

            user_id = payload.get('uid')
            user = users.filter(id=user_id)
            if users.filter(id=user_id).exists():
                request.jti = jti
                return (user, None)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.exceptions.PyJWTError:
            raise ValidationError('Token validation error')
        except Exception as exception:
            raise AuthenticationFailed(exception)
