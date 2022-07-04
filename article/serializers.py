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
    username = serializers.SerializerMethodField()
    def get_username(self,obj):
        
        return obj.user.fullname

    # user = serializers.SlugRelatedField(read_only=True, slug_field='fullname')  # id 값 안나올 시 삭제 ! 
    # user =  serializers.RelatedField(many=True, read_only='True')


    class Meta:
        model = CommentModel
        fields = ["article", "content", "modlfied_at", "user", "username"]


class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source="comment_set")
    bookmarks = BookMarkSerializer(many=True, read_only=True, source="bookmark_set")
    likes = LikeSerializer(many=True, read_only=True, source="like_set")
    username = serializers.SerializerMethodField()

    def get_username(self, obj):

        return obj.user.fullname


    # image =
    class Meta:
        model = ArticleModel
        fields = ["id", "title", "content", "created_at", "modlfied_at",
                  "comments", "username", "user", "comments", "bookmarks", "likes"] 



