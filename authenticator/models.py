import uuid

from django.db import models
from django.contrib.auth.models import User


class TokenBlackList(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  jti = models.CharField(max_length=1000)
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
  create_at = models.DateTimeField(auto_now_add=True)