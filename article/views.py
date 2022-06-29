from django.shortcuts import render
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import article
from article.models import Article as ArticleModel
from article.serializers import ArticleSerializer


class ArticleView(APIView):
    def get(self, request):
        articles = ArticleModel.objects.all()
        serialized_data = ArticleSerializer(articles, many=True).data
        return Response(serialized_data)
    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        article_serializer = ArticleSerializer(data=data)
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        return Response({'message': 'Good~! put'}, status=status.HTTP_200_OK)