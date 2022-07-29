from django.db import models


class News(models.Model):
    title = models.TextField()
    desc = models.TextField(null=True)
    url = models.CharField(max_length=200)