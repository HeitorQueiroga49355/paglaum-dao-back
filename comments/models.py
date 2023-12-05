from django.db import models
from account.models import User
from articles.models import Article
from datetime import datetime
from django.utils import timezone

class Comment(models.Model):
    text = models.TextField(max_length=5000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    publication_date = models.DateTimeField(blank=False, default=timezone.now)
    last_edition = models.DateTimeField(blank=False, default=timezone.now)
    of_article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
