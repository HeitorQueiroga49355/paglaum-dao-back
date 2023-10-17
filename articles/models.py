from django.db import models

class Article(models.Model):
    message = models.CharField(max_length=20)
