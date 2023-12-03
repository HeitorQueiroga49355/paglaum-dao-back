from django.db import models
from account.models import User

class Comment(models.Model):
    text = models.TextField(max_length=5000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)
