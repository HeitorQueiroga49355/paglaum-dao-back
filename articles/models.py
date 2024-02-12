from django.db import models
from account.models import User
from datetime import datetime
from core.utils import unique_slug_generator
from django.db.models.signals import pre_save


class Article(models.Model):
    title = models.TextField(blank=False)
    subtitle = models.TextField(blank=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    content = models.TextField(blank=False)
    publication_date = models.DateTimeField(blank=False, default=datetime.now)
    last_edition = models.DateTimeField(blank=False, default=datetime.now)
    active = models.BooleanField(default=True)
    cover_image = models.ImageField(blank=True)
    is_emphasis = models.BooleanField(default=False)
    slug = models.SlugField(max_length=300, null=True, blank=True)

    def get_publication_date(self):
        return self.publication_date


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Article)
