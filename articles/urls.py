from django.urls import path
from .views import ArticleAPIView, ArticleUniqueApiView

urlpatterns = [
    path('article/', ArticleAPIView.as_view(), name="articles"),
    path('article/<int:pk>', ArticleUniqueApiView.as_view(), name="article_dynamic"),
]
