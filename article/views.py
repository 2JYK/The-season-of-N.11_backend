from django.shortcuts import render
from datetime import datetime
from django.db.models.query_utils import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from article.serializers import ArticleSerializer
from article.serializers import CommentSerializer
from article.serializers import LikeSerializer
from article.serializers import BookMarkSerializer

from article.models import Article as ArticleModel
from article.models import Comment as CommentModel
from article.models import Like as LikeModel
from article.models import BookMark as BookMarkModel

from rest_framework_simplejwt.authentication import JWTAuthentication


class ArticleView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        articles = ArticleModel.objects.all()
        
        serialized_data = ArticleSerializer(articles, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)
   
    def post(self, request):
        
        data = request.data    
        data["user"] = request.user.id
        article_serializer = ArticleSerializer(data=data)

        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)
        article_serializer = ArticleSerializer(article, data=request.data, partial=True)

        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id):
        article = ArticleModel.objects.get(id=article_id)
        article.delete()
        return Response({"message": "해당 게시글이 삭제 되었습니다."}, status=status.HTTP_200_OK)


class CommentView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        comment = CommentModel.objects.all()
        serialized_data = CommentSerializer(comment, many=True).data
        
        return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        request.data["user"] = request.user.id
        print(request.data["user"])
        comment_serializer = CommentSerializer(data=request.data)

        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, comment_id):
        comment = CommentModel.objects.get(id=comment_id)
        comment_serializer = CommentSerializer(comment, data=request.data, partial=True)
    
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
    
        return Response(comment_serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, comment_id):
        comment = CommentModel.objects.get(id=comment_id)
        comment.delete()
        return Response({"message": "해당 댓글이 삭제 되었습니다."}, status=status.HTTP_200_OK)


class BookMarkView(APIView):
    def get(self, request):
        book_mark = BookMarkModel.objects.all()
        serialized_data = BookMarkSerializer(book_mark, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data["user"] = request.user.id
        bookmark_serializer = BookMarkSerializer(data=request.data)
        existed_bookmark = BookMarkModel.objects.filter(
            Q(user_id=request.user.id) & Q(article_id=request.data["article"])
            )
        if existed_bookmark:
            existed_bookmark.delete()
            return Response({"message":"북마크가 취소 되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        elif bookmark_serializer.is_valid():
            bookmark_serializer.save()
        return Response(bookmark_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, bookmark_id):
        book_mark = BookMarkModel.objects.get(id=bookmark_id)
        book_mark.delete()
        return Response({"message": "해당 북마크가 해제 되었습니다."}, status=status.HTTP_200_OK)


class LikeView(APIView):
    def get(self, request):
        like = LikeModel.objects.all()
        serialized_data = LikeSerializer(like, many=True).data

        return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        like_serializer = LikeSerializer(data=request.data)
        existed_like = LikeModel.objects.filter(
            Q(user_id=request.user.id) & Q(article_id=request.data["article"])
            )

        if existed_like:
            existed_like.delete()
            return Response({"message":"이미 좋아요 했슈"}, status=status.HTTP_400_BAD_REQUEST)
        
        elif like_serializer.is_valid():
            like_serializer.save()
        return Response(like_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, like_id):
        like = LikeModel.objects.get(id=like_id)
        like.delete()
        return Response({"message": "해당 게시글에 좋아요를 취소했습니다."}, status=status.HTTP_200_OK)