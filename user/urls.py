from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserView.as_view()),
    path('login/', views.UserAPIView.as_view()),
    path('logout/', views.UserAPIView.as_view()),
]

