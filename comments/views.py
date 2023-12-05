from .models import Comment
from .serializers import CommentSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

JWT_authenticator = JWTAuthentication()

class CommentListCreateAll(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        try:
            article_pk = self.kwargs.get('article_pk')
            if article_pk is not None:
                queryset = self.get_queryset().all().filter(of_article=article_pk)
                serializer = CommentSerializer(queryset, many=True)
                return Response(serializer.data, status=200)
            else:
                user, validated_token = JWT_authenticator.authenticate(request)
                if user.is_staff:
                    return super().get(request, *args, **kwargs)
                else:
                    return Response({'detail': 'You don\'t have permission for this'}, status=401)
        except Exception as error:
            print(error)
            return Response({'detail': 'Authorization bearer token not provided'}, status=403)
