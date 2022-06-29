from django.contrib import admin
from django.urls import path, include
from article import views


urlpatterns = [
    path('', views.ArticleView.as_view()),
    path('comment/', views.CommentView.as_view()),
    path('bookmark/', views.BookMarkView.as_view()),
    path('like/', views.LikeView.as_view()),
    path('comment/<comment_id>/', views.CommentView.as_view()),
    path('bookmark/<bookmark_id>/', views.BookMarkView.as_view()),
    path('like/<like_id>/', views.LikeView.as_view()),
]