from .views import ArticleListCreate, ArticleRetrievePatchDelete, ArticleEmphasisView, ArticleDeepDelete
from django.urls import path

urlpatterns = [
    path('articles/', ArticleListCreate.as_view(), name="create_list_articles"),
    path('articles/<int:pk>/', ArticleRetrievePatchDelete.as_view(),
         name="retrieve_delete_update_article"),
    path('articles/emphasis/', ArticleEmphasisView.as_view(),
         name="list_emphasis_articles"),
    path('articles/make_emphasis/<int:pk>/',
         ArticleEmphasisView.as_view(), name="make_emphasis"),
    path('author/<int:author_pk>/articles/',
         ArticleListCreate.as_view(), name="make_emphasis"),
    path('articles/<int:pk>/deep_delete/',
         ArticleDeepDelete.as_view(), name="deep_delete_article")
]
