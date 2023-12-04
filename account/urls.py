from .views import (UserListCreate, SendEmailConfirmationTokenAPIView,
                    UserRetrieveUpdate, confirm_email_view)
from django.urls import path

urlpatterns = [
    path('user/', UserListCreate.as_view(), name="create_list _users"),
    path('user/me', UserRetrieveUpdate.as_view(), name="create_list_users"),
    path('send-confirmation-email/',
         SendEmailConfirmationTokenAPIView.as_view(), name="check_user_email"),
    path('confirm-email/', confirm_email_view, name='confirm_email_view')
]
