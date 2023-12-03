from .views import ArticleListCreate, ArticleRetrievePatchDelete
from django.urls import path

urlpatterns = [
    path('articles/', ArticleListCreate.as_view(), name="create_list_articles" ),
    path('articles/<int:pk>/', ArticleRetrievePatchDelete.as_view(), name="retrieve_delete_update_article")
]
