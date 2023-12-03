from django.contrib import admin
from .models import User


@admin.register(User)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'is_trusty',
    )
