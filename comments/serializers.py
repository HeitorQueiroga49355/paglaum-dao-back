from rest_framework import serializers
from .models import Comment
from account.serializers import UserSerializerBasicData


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializerBasicData(many=False, read_only=False)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'active',
            'publication_date',
            'last_edition',
        )


class CommentSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'active',
            'publication_date',
            'last_edition',
            'of_article',
        )
