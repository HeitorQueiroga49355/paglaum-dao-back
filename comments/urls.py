from .views import CommentListCreateAll, CommentRetrieveUpdateDelete
from django.urls import path

urlpatterns = [
    path('comments/all/', CommentListCreateAll.as_view(), name='list_all_comments'),
    path('comments/<int:pk>', CommentRetrieveUpdateDelete.as_view(), name="update_retrieve_delete_comments"),
    path('article/<int:article_pk>/comments', CommentListCreateAll.as_view(), name='list_comments_by_article'),
]