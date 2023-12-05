from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'active',
            'publication_date',
            'last_edition'
        )
