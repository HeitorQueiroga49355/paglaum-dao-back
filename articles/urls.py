from django.urls import path
from .views import GenericUniqueApiView, GenericAPIView

urlpatterns = [
    path('article/', GenericAPIView.as_view(), name="articles"),
    path('comment/', GenericAPIView.as_view(), name="comments"),
    path('user/', GenericAPIView.as_view(), name='users'),
    path('article/<int:pk>', GenericUniqueApiView.as_view(), name="article_dynamic"),
    path('comment/<int:pk>', GenericUniqueApiView.as_view(), name="comments"),
    path('comment/<int:pk>', GenericUniqueApiView.as_view(), name="comments"),
]
