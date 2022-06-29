from rest_framework import serializers
from article.models import Article as ArticleModel
from article.models import Comment as CommentModel
from user.serializers import UserSerializer



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentModel
        fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    user = UserSerializer()
    # image =
    class Meta:
        model = ArticleModel
        fields = ["title", "content", "created_at", "modlfied_at", "comment_set", "user"]