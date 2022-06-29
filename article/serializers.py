from rest_framework import serializers
from article.models import Article as ArticleModel
# from user.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # image =
    class Meta:
        model = ArticleModel
        fields = ["title", "content", "created_at", "modlfied_at"]