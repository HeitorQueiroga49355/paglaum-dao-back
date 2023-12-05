from .models import Comment
from .serializers import CommentSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from copy import copy

JWT_authenticator = JWTAuthentication()


class CommentListCreateAll(generics.ListCreateAPIView):
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
            return Response({'detail': 'Authorization bearer token not provided'}, status=403)

    def post(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            article_pk = self.kwargs.get('article_pk')
            request.data.update({
                'author': user.pk,
                'publication_date': datetime.now(),
                'last_edition': datetime.now(),
                'of_article': article_pk, 
                'active': True
            })
            return super().create(request, *args, **kwargs)
        except TypeError as error:
            return Response({'detail': 'Authorization bearer token was not provided'}, status=403)
        except Exception as error:
            print(error)
            return Response({'detail': 'Something went wrong'}, status=500)


class CommentRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            pk_comment = self.kwargs.get('pk')
            comment = self.get_queryset().all().filter(id=pk_comment)
            if len(comment) != 1:
                return Response({'detail': 'Comment not found'}, status=404)
            if comment[0].author == user:
                request.data['author'] = user.pk
                request.data['publication_date'] = comment[0].publication_date
                request.data['last_edition'] = datetime.now
                request.data['of_article'] = comment[0].publication_date
                request.data['active'] = comment[0].active
                return super().partial_update(request, *args, **kwargs)
            else:
                return Response({'detail': 'You don\'t have permission for this'}, status=401)
        except TypeError as error:
            return Response({'detail': 'Authorization bearer token was not provided'}, status=403)
        except Exception as error:
            return Response({'detail': 'Something went wrong'}, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            pk_comment = self.kwargs.get('pk')
            comment = self.get_queryset().all().filter(id=pk_comment)
            if comment[0].author == user or user.is_staff:
                request.data.update({'active': False})
                return super().patch(request, *args, *kwargs)
            else:
                return Response({'detail': 'You don\'t have permission for this '}, status=401)
        except Exception as error:
            return Response({'detail': 'Something went wrong'}, status=500)
