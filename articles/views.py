from .models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from account.models import User

JWT_authenticator = JWTAuthentication()

class ArticleListCreate(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def post(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            request.data.update({'author': user.id})
        except:
            return Response({'detail': 'Authorization bearer token not provided'}, status=403)
        return super().post(request, *args, **kwargs)


class ArticleRetrievePatchDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def patch(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            request.data.update({'author': user.id})
            request.data.update({'last_edition': datetime.now()})

            obj_to_path = self.get_queryset().filter(id=self.kwargs.get('pk'))
            if (len(obj_to_path) != 1):
                return Response({'detail': 'object not found'}, status=404)

            request.data.update(
                {'publication_date': obj_to_path[0].get_publication_date()})
        except Exception as error:
            return Response({'detail': error}, status=403)
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            if(user.is_staff):
                request.data.update({'activate': False})
                return super().patch(request, *args, **kwargs)
            else:
                return Response({'detail': 'Authorization bearer token not provided'}, status=403)
        except:
            return Response({'detail': 'Authorization bearer token not provided'}, status=403)
