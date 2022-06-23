from django.db import models

# Create your models here.
class News(models.Model):
    title =  models.TextField()
    desc = models.TextField(null=True)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.title