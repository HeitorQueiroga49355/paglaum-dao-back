from django.contrib import admin
from .models import User, EmailConfirmationToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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

@admin.register(EmailConfirmationToken)
class EmailTokenAdmin(admin.ModelAdmin):
    list_display = (
       'id',
       'created_at',
       'user',
    )
