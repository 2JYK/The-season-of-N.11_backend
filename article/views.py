from datetime import datetime
from django.db.models.query_utils import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from article.serializers import ArticleSerializer
from article.serializers import CommentSerializer
from article.serializers import LikeSerializer
from article.serializers import BookMarkSerializer
from article.serializers import ImageSerializer

from article.models import Style as StyleModel
from article.models import Image as ImageModel
from article.models import Article as ArticleModel
from article.models import Comment as CommentModel
from article.models import Like as LikeModel
from article.models import BookMark as BookMarkModel

from user.models import User as UserModel

import cv2 
import numpy as np


def magic(filestr, style):
    npimg = np.fromstring(filestr, np.uint8)
    input_img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    style = cv2.dnn.readNetFromTorch(f'article/models/{style}')
    
    h, w, c = input_img.shape
    input_img = cv2.resize(input_img, dsize=(500, int(h / w * 500)))
    MEAN_VALUE = [103.939, 116.779, 123.680]
    blob = cv2.dnn.blobFromImage(input_img, mean=MEAN_VALUE)
    style.setInput(blob)
    output = style.forward()
    output = output.squeeze().transpose((1, 2, 0)) 
    output += MEAN_VALUE 
    output = np.clip(output, 0, 255) 
    output = output.astype('uint8')
    
    time = datetime.now().strftime('%Y-%m-%d%H:%M:%s')
    cv2.imwrite(f'output/{time}.jpeg', output) 
    result = f'output/{time}.jpeg'

    return result
    
    
class ArticleView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        articles = ArticleModel.objects.all().order_by('-created_at')
        serialized_data = ArticleSerializer(articles, many=True).data

        return Response(serialized_data, status=status.HTTP_200_OK)
   
    def post(self, request):
        data = request.data  
        style_info = StyleModel.objects.get(category=request.data["style"])
        output_img = magic(
                filestr=request.FILES['input'].read(),
                style=request.data.get('style', '') 
            )
        image_info = ImageModel.objects.create(style=style_info, output_img=output_img)
        image_info.save()

        data = {
            "user" : request.user.id,
            "style" : style_info,
            "image" : output_img,
            "title" : request.data["title"],
            "content" : request.data["content"]
        }

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
        user = request.user.id
        article = ArticleModel.objects.get(id=article_id)
        
        if article.user.id == user:
            article.delete()
            return Response({"message": "해당 게시글이 삭제 되었습니다."}, status=status.HTTP_200_OK)
        
        else :
            return Response({"message": "게시글 작성자가 아닙니다"}, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        comment = CommentModel.objects.all()
        serialized_data = CommentSerializer(comment, many=True).data
        
        return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data["user"] = request.user.id
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
        user = request.user.id
        comment = CommentModel.objects.get(id=comment_id)
        
        if comment.user.id == user:
            comment.delete()
            return Response({"message": "해당 댓글이 삭제 되었습니다."}, status=status.HTTP_200_OK)
        
        else :
            return Response({"message": "댓글 작성자가 아닙니다"}, status=status.HTTP_400_BAD_REQUEST)


class BookMarkView(APIView):
    authentication_classes = [JWTAuthentication]
    
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
    authentication_classes = [JWTAuthentication]
    
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


#ㅡ 마이페이지 ㅡ#
class MyPageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user.id
        articles = ArticleModel.objects.filter(user_id=user).order_by('-id')
        serialized_data = ArticleSerializer(articles, many=True).data
        
        return Response(serialized_data, status=status.HTTP_200_OK)


#ㅡ 북마크 ㅡ#
class MyBookMarkView(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        user = request.user.id
        bookmarks = BookMarkModel.objects.filter(user_id=user).order_by('-id')

        serialized_data = BookMarkSerializer(bookmarks, many=True).data
        
        return Response(serialized_data, status=status.HTTP_200_OK)
    



