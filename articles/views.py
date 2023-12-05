from .models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime

JWT_authenticator = JWTAuthentication()


class ArticleListCreate(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def post(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            request.data.update({'author': user.id})
            return super().post(request, *args, **kwargs)
        except:
            return Response({'detail': 'Authorization bearer token not provided'}, status=403)


class ArticleRetrievePatchDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def patch(self, request, make_emphasis=False, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
        except:
            return Response({'detail': 'Authorization bearer token was not provided'}, status=403)
        print(kwargs)
        try:
            obj_to_path = self.get_queryset().filter(id=self.kwargs.get('pk'))
            if (len(obj_to_path) != 1):
                return Response({'detail': 'object not found'}, status=404)
            else:
                request.data.update(
                    {'publication_date': obj_to_path[0].get_publication_date(),
                     'author': user.id,
                     'last_edition': datetime.now()})
                return super().partial_update(request, *args, **kwargs)
        except Exception as error:
            return Response({'detail': error}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            if (user.is_staff):
                request.data.update({'activate': False})
                return super().patch(request, *args, **kwargs)
            else:
                return Response({'detail': 'Authorization bearer token not provided'}, status=403)
        except:
            return Response({'detail': 'Authorization bearer token not provided'}, status=403)


class ArticleEmphasisView(mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().all().filter(is_emphasis=True)
        emphasis_articles = ArticleSerializer(queryset, many=True)
        return Response(emphasis_articles.data, status=200)