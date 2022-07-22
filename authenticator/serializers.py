from unittest.util import _MAX_LENGTH
from click import password_option
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=50)
  password = serializers.CharField(max_length=50)