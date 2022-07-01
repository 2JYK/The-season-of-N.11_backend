from rest_framework import serializers
from article.models import Style as StyleModel
from article.models import Image as ImageModel
from article.models import Article as ArticleModel
from article.models import Comment as CommentModel
from article.models import Like as LikeModel
from article.models import BookMark as BookMarkModel


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleModel
        fields = "__all__"
        
        
class ImageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
    
    class Meta:
        model = ImageModel
        fields = "__all__" # user / style / output_img(imagefield)
        
        
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
    image = ImageSerializer(many=True)
    
    class Meta:
        model = ArticleModel
        fields = ["id", "title", "content", "created_at", "modlfied_at",
                  "comments", "user", "image"] 
