from django.db import models


class News(models.Model):
    title = models.TextField()
    desc = models.TextField(null=True)
    url = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)