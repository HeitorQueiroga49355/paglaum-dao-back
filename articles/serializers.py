from rest_framework import serializers
from .models import Article
from account.serializers import UserSerializerBasicData, UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer

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


class ArticleSerializerList(serializers.ModelSerializer):
    content = serializers.CharField(max_length=None, write_only=True)
    author = UserSerializerBasicData(many=False, read_only=False)

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

class ArticleSerializerCreate(serializers.ModelSerializer):
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
