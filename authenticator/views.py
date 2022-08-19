from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from authenticator.models import TokenBlackList

from authenticator.serializers import LoginSerializer
from authenticator.utils import token_generator


class Login(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return Response({
                "message": "Username or password is incorrect"
            }, status=status.HTTP_400_BAD_REQUEST)
        token = token_generator(user)
        return Response({
            "access-token": token,
            "message": "login success"
        })

class Logout(APIView):

    def post(self, request):
        TokenBlackList.objects.create(id=request.jti, 
                                      user_id=request.uid)
        return Response({
            "message": "Logout Successful."
        })
