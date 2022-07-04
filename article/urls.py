from django.contrib import admin
from django.urls import path
from article import views

from django.conf.urls.static import static
from django.conf import settings

# MEDIA_URL로 들어오는 요청에 대해 MEDIA_ROOT 경로를 탐색한다.


urlpatterns = [
    path('', views.ArticleView.as_view()),
    path('comment/', views.CommentView.as_view()),
    path('bookmark/', views.BookMarkView.as_view()),    
    path('mypage/', views.MypageView.as_view()),
    path('like/', views.LikeView.as_view()),
    path('<article_id>/', views.ArticleView.as_view()), 
    path('comment/<comment_id>/', views.CommentView.as_view()),
    path('bookmark/<bookmark_id>/', views.BookMarkView.as_view()),
    path('like/<like_id>/', views.LikeView.as_view()),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


