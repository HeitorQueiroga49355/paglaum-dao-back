from rest_framework import serializers
from .models import Article
from account.serializers import UserSerializerBasicData, UserSerializer
from env import API_BASE


class ArticleSerializerDetailed(serializers.ModelSerializer):
    author = UserSerializer()

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
    cover_image = serializers.SerializerMethodField()

    def get_cover_image(self, article):
        photo_url = article.cover_image
        return API_BASE + 'media/' + str(photo_url)

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

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['cover_image'] = self.content['cover_image'].build_absolute_uri(
    #         representation['cover_image'])
    #     return representation


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
