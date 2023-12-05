from django.db import models
from account.models import User
from articles.models import Article

class Comment(models.Model):
    text = models.TextField(max_length=5000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    of_article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
