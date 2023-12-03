from .models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

JWT_authenticator = JWTAuthentication()

class ArticleListCreate(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # http_method_names = ['get', 'head', 'options']

    def post(self, request, *args, **kwargs):
        try:
            user, validated_token = JWT_authenticator.authenticate(request)
        except:
            return Response({"message": "Authorization token not provided"}, status=401)
        return super().post(request, *args, **kwargs)
