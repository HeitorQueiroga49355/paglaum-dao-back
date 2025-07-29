from .views import ArticleListCreate, ArticleRetrievePatchDelete, ArticleEmphasisView, ArticleDeepDelete, ActivateArticle
from django.urls import path

urlpatterns = [
    path('articles/', ArticleListCreate.as_view(), name="create_list_articles"),
    path('articles/emphasis/', ArticleEmphasisView.as_view(),
         name="list_emphasis_articles"),
    path('articles/<slug:slug>/', ArticleRetrievePatchDelete.as_view(),
         name="retrieve_deactivate_update_article"),
    path('articles/make_emphasis/<int:pk>/',
         ArticleEmphasisView.as_view(), name="make_emphasis"),
    path('author/<int:author_pk>/articles/',
         ArticleListCreate.as_view(), name="make_emphasis"),
    path('articles/<int:pk>/deep_delete/',
         ArticleDeepDelete.as_view(), name="deep_delete_article"),
    path('articles/<slug:slug>/activate', ActivateArticle.as_view(), name="activate_article"),
]
