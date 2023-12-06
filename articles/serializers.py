from rest_framework import serializers
from .models import Article
from account.serializers import UserSerializerBasicData


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializerBasicData(read_only=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'subtitle',
            'author',
            'publication_date',
            'last_edition',
            'activate',
            'content',
            'cover_image',
            'is_emphasis',
        )


class ArticleSerializerMainPage(serializers.ModelSerializer):
    content = serializers.CharField(max_length=None, write_only=True)
    author = UserSerializerBasicData()

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'subtitle',
            'author',
            'publication_date',
            'last_edition',
            'activate',
            'content',
            'cover_image',
            'is_emphasis',
        )
