from email import message
from django.shortcuts import render
from django.contrib.auth.models import User
from requests import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
from articlescraper import serializers
from .serializers import LoginSerializer

# Create your views here.


class Login(APIView):
    queryset = User.objects.all()
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
          return Response({
                "message": "Username or password is incorrect"
            }, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            "uid": user.id,
            "username": username
        }
        
        key = 'thisisakey'
        token = jwt.encode(payload, key)

        return Response({
            "access-token": token,
            "message": "login success"
        })
