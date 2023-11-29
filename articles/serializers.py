from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'subtitle',
            'author',
            'publication_date',
            'last_edition',
        )
