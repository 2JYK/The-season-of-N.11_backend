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
        fields = "__all__" 
        
        
class BookMarkSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_title(self, obj):
        return obj.article.title  
    
    def get_content(self, obj):
        return obj.article.content
    
    def get_comments(self, obj):
        comment_list = []
        for comments in obj.article.comment_set.all():
            username = comments.user.username
            content = comments.content
            time_post = comments.modlfied_at.replace(microsecond=0).isoformat()
            comment_list.append({'username': username, 'content': content, 'modlfied_time': time_post})
        return comment_list
    
    def get_image(self, obj):
        return obj.article.image
    class Meta:
        model = BookMarkModel
        fields = ["user", "id", "username", "article", "title", "content", "comments", "image"]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    modlfied_time = serializers.SerializerMethodField()
    
    def get_username(self,obj):
        return obj.user.fullname
    
    def get_modlfied_time(self, obj):
        modlfied_time = obj.modlfied_at.replace(microsecond=0).isoformat()
        return modlfied_time
    
    class Meta:
        model = CommentModel
        fields = ["id", "article", "content", "user", "username", "modlfied_at", "modlfied_time"]


class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True, source="comment_set")
    bookmarks = BookMarkSerializer(many=True, read_only=True, source="bookmark_set")
    likes = LikeSerializer(many=True, read_only=True, source="like_set")
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.fullname

    class Meta:
        model = ArticleModel
        fields = ["id", "title", "content", "created_at", "modlfied_at",
                  "comments", "username", "user", "comments", "bookmarks", "likes", "image"] 
