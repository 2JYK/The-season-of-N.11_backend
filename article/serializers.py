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
    class Meta:
        model = CommentModel
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = ArticleModel
        fields = ["title", "content", "created_at", "modlfied_at", "comment_set", "user"]