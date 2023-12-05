from .views import CommentListCreateAll
from django.urls import path

urlpatterns = [
    path('comments/all/', CommentListCreateAll.as_view(), name='list_all_comments'),
    path('article/<int:article_pk>/comments', CommentListCreateAll.as_view(), name='list_comments_by_article'),
    path('')
]