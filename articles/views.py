from .models import Article
from .serializers import ArticleSerializerDetailed, ArticleSerializerList, ArticleSerializerCreate
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime

JWT_authenticator = JWTAuthentication()


class ArticleListCreate(generics.ListCreateAPIView):
    queryset = Article.objects.all().order_by('-publication_date')
    serializer_class = ArticleSerializerList

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        if author_pk is not None:
            limit = request.query_params.get('limit', 20)
            offset = request.query_params.get('offset', 0)

            try:
                limit = int(limit)
                offset = int(offset)
            except ValueError:
                return Response({'detail': 'Invalid limit or offset values'}, status=400)
            all_queryset = self.get_queryset().all().filter(author__id=author_pk)
            count = all_queryset.count()
            queryset = all_queryset[offset:offset + limit]
            serializer = ArticleSerializerList(queryset, many=True)
            return Response({'count': count, 'results': serializer.data}, status=200)
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            request.data.update({'author':  user.id,
                                 'publication_date': datetime.now(),
                                 'last_edition': datetime.now(),
                                 'activate': True})
            serializer = ArticleSerializerCreate(data=request.data)
            serializer.is_valid(raise_exception=True)
            article = serializer.save()

            return Response(serializer.data, status=201)
        except Exception as error:
            return Response({'detail': 'Authorization bearer token not provided'}, status=403)


class ArticleRetrievePatchDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializerDetailed

    def patch(self, request, make_emphasis=False, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
        except:
            return Response({'detail': 'Authorization bearer token was not provided'}, status=403)
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
    serializer_class = ArticleSerializerDetailed

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().all().filter(is_emphasis=True)
        emphasis_articles = ArticleSerializerDetailed(queryset, many=True)
        return Response(emphasis_articles.data, status=200)

    def patch(self, request, *args, **kwargs):
        article_pk = self.kwargs.get('pk')
        queryset = self.get_queryset().all().filter(id=article_pk)
        user, validated_token = JWT_authenticator.authenticate(request)

        if not user.is_staff:
            return Response({'detail': 'You don\'t have permission for this'}, status=401)

        if (len(queryset) != 1):
            return Response({'detail': 'Article not found'}, status=404)
        request.data.update({})
        print('here')
        if queryset[0].is_emphasis:
            request.data.update({'is_emphasis': False})
        else:
            request.data.update({'is_emphasis': True})

        return super().partial_update(request, *args, **kwargs)
