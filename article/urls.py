from django.urls import path
from article import views


urlpatterns = [
    path("", views.ArticleView.as_view()),
    path("comment/", views.CommentView.as_view()),
    path("bookmark/", views.BookMarkView.as_view()),    
    path("mybookmark/", views.MyBookMarkView.as_view()),
    path("like/", views.LikeView.as_view()),
    path("mypage/", views.MyPageView.as_view()),
    path("<article_id>/", views.ArticleView.as_view()), 
    path("comment/<comment_id>/", views.CommentView.as_view()),
    path("bookmark/<bookmark_id>/", views.BookMarkView.as_view()),
    path("like/<like_id>/", views.LikeView.as_view()),
] 
