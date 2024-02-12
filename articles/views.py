from .models import Article
from .serializers import ArticleSerializerDetailed, ArticleSerializerList, ArticleSerializerCreateAndUpdate
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
from account.utils import GhostUserClass
from django.core.files.storage import FileSystemStorage

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
            try:
                user, validated_token = JWT_authenticator.authenticate(request)
                # user = {'is_staff': True}
            except:
                user = GhostUserClass()
            if user.is_staff:
                articles = self.queryset.filter()
            else:
                articles = self.queryset.filter(active=True)
            return Response({'results': self.serializer_class(articles, many=True).data}, status=200)

    def post(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            request.data.update({'author':  user.id,
                                 'publication_date': datetime.now(),
                                 'last_edition': datetime.now(),
                                 'active': True})
            serializer = ArticleSerializerCreateAndUpdate(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({'detail': 'Successful article creation'}, status=201)
        except Exception as error:
            print(error)
            return Response({'detail': 'Authorization bearer token not provided'}, status=403)


class ArticleRetrievePatchDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializerDetailed

    def patch(self, request, make_emphasis=False, *args, **kwargs):
        request.data._mutable = True
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
        except:
            return Response({'detail': 'Authorization bearer token was not provided'}, status=403)
        try:
            article = self.get_queryset().filter(id=self.kwargs.get('pk'))
            if (len(article) != 1):
                return Response({'detail': 'object not found'}, status=404)
            else:
                if (article[0].author == user or user.is_staff):
                    request.data.update({
                        'publication_date': article[0].get_publication_date(),
                        'author': user.id,
                        'last_edition': datetime.now()
                    })
                    return super().partial_update(request, *args, **kwargs)
                else:
                    return Response({'detail': "You don't have permission for this"}, status=401)
        except Exception as error:
            return Response({'detail': str(error)}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
            article = self.get_queryset().filter(id=self.kwargs.get('pk'))
            if (user.is_staff or article.author == user):
                request.data.update({'active': False})
                print('here3')
                return super().patch(request, *args, **kwargs)
            else:
                return Response({'detail': 'Authorization bearer token not provided'}, status=403)
        except Exception as error:
            return Response({'detail': str(error)}, status=403)


class ArticleDeepDelete(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializerDetailed

    def delete(self, request, *args, **kwargs):
        user, validated_token = JWT_authenticator.authenticate(request)
        if (user.is_staff):
            pk = self.kwargs.get('pk')
            article = self.queryset.get(pk=pk)
            fs = FileSystemStorage()
            print(article.cover_image.path)
            fs.delete(article.cover_image.path)
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({'detail': 'You don\'t have permission for this'}, status=403)


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
        if queryset[0].is_emphasis:
            request.data.update({'is_emphasis': False})
        else:
            request.data.update({'is_emphasis': True})

        return super().partial_update(request, *args, **kwargs)
