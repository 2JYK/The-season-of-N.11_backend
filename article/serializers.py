from rest_framework import serializers
from article.models import Article as ArticleModel
from article.models import Comment as CommentModel
from article.models import Like as LikeModel
from article.models import BookMark as BookMarkModel
from user.serializers import UserSerializer


class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMarkModel
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):

    # user = serializers.SlugRelatedField(read_only=True, slug_field='fullname')  # id 값 안나올 시 삭제 ! 
    class Meta:
        model = CommentModel
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source="comment_set")
    
    # user = UserSerializer(many=True)
    # image =
    class Meta:
        model = ArticleModel
        fields = ["id", "title", "content", "created_at", "modlfied_at",
                  "comments", "user"] 
