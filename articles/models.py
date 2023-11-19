from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Article(models.Model):
    title = models.TextField(default='')
    subtitle = models.TextField(default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    publication_date = models.DateTimeField(blank=True, default=datetime.now)
    last_edition = models.DateTimeField(blank=True, default=datetime.now)
