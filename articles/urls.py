from .views import ArticleListCreate, ArticleRetrievePatchDelete, ArticleEmphasisView
from django.urls import path

urlpatterns = [
    path('articles/', ArticleListCreate.as_view(), name="create_list_articles" ),
    path('articles/<int:pk>/', ArticleRetrievePatchDelete.as_view(), name="retrieve_delete_update_article"),
    path('articles/emphasis/', ArticleEmphasisView.as_view(), name="list_emphasis_articles"),
    path('articles/make_emphasis/<int:pk>/', ArticleEmphasisView.as_view(), name="make_emphasis"),
]
