from .views import ArticleListCreate
from rest_framework.routers import SimpleRouter
from django.urls import path

urlpatterns = [
    path('article/', ArticleListCreate.as_view(), name="list_articles" )
]
