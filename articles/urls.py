from django.urls import path
from .views import GenericAPIView

urlpatterns = [
    path('article/', GenericAPIView.as_view(), name="articles"),
    path('comment/', GenericAPIView.as_view(), name="comments"),
    path('user/', GenericAPIView.as_view(), name='users'),
    path('article/<int:id>', GenericAPIView.as_view(), name="article_dynamic"),
    path('comment/<int:id>', GenericAPIView.as_view(), name="comments"),
    path('comment/<int:id>', GenericAPIView.as_view(), name="comments"),
]
