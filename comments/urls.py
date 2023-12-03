from .views import CommentViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('comments', CommentViewSet)