from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer


class GenericAPIView(APIView):
    def get(self, request, id=None):
        if (id != None):
            articles = Article.objects.all().filter(id=id)
            if(articles.__len__() == 0):
                return Response({'message': 'not found'}, status=404)
        else:
            articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def delete(self, request):
        return Response({'message': 'successful'})

    def post(self, request):
        return Response({'message': 'successful'})

    def put(self, request):
        return Response({'message': 'successful'})

    def patch(self, request):
        return Response({'message': 'successful'})
