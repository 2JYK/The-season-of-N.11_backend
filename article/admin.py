from django.contrib import admin
from article.models import Article as ArticleModel
from article.models import Comment as CommentModel
from article.models import Like as LikeModel
from article.models import BookMark as BookMarkModel 
from django.contrib import admin


# Bookmark클래스와 BookmarkAdmin클래스를 등록
admin.site.register(BookMarkModel)
admin.site.register(ArticleModel)
admin.site.register(CommentModel)
admin.site.register(LikeModel)