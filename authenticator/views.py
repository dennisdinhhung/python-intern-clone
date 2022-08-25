from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from authenticator.models import TokenBlackList
from authenticator.serializers import LoginSerializer
from authenticator.utils import token_generator


class Login(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = User.objects.filter(username=username).first()
        if not user or (user and not user.check_password(password)):
            raise ValidationError({"message":"Username or Password is incorrect."})
        
        exp_time = settings.JWT_EXP_MINUTE
        user_id = user.id
        token = token_generator(user_id, exp_time)
        return Response({
            "access_token": token,
            "message": "login success"
        })

class Logout(APIView):

    def post(self, request):
        jti = request.jti
        user_id = request.uid
        TokenBlackList.objects.create(jti = jti, user_id = user_id)
        return Response({
            "message": "Logout Successful."
        })
