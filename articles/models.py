from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Article(models.Model):
    title = models.TextField(blank=False)
    subtitle = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    content = models.TextField(blank=False)
    publication_date = models.DateTimeField(blank=False, default=datetime.now)
    last_edition = models.DateTimeField(blank=False, default=datetime.now)
