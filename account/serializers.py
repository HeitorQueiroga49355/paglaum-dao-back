from rest_framework import serializers
from .models import User
from env import API_BASE


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserSerializerProtected(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'last_login',
                  'is_superuser',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'is_staff',
                  'is_active',
                  'date_joined',
                  'is_trusty',
                  'image_profile',
                  'biography',)
        extra_kwargs = {field: {'read_only': True} for field in fields}


class UserSerializerBasicData(serializers.ModelSerializer):
    image_profile = serializers.SerializerMethodField()

    def get_image_profile(self, user):
        photo_url = user.image_profile
        return API_BASE + 'media/' + str(photo_url)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'image_profile',
        )
