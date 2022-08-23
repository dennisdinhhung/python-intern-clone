from django.db import models


class NewsArticles(models.Model):
    
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)