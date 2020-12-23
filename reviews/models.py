from django.db import models
from django.conf import settings

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
