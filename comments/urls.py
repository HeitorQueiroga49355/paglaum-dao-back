from django.urls import path
from .views import CommentAPIView, CommentUniqueApiView

urlpatterns = [
    path('comment/', CommentAPIView.as_view(), name="comments"),
    path('comment/<int:pk>', CommentUniqueApiView.as_view(), name="comments"),
]
