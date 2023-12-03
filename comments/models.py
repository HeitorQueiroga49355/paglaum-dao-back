from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    text = models.TextField(max_length=5000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)

class Teste(models.Model):
    teste = models.TextField(max_length=100)