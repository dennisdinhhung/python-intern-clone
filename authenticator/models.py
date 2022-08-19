from django.db import models
import uuid

from django.contrib.auth.models import User
class TokenBlackList(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
  create_at = models.DateTimeField(auto_now_add=True)