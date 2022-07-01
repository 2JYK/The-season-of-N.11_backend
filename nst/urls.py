from django.urls import path
from nst import views

urlpatterns = [
    path('', views.NstView.as_view()),
]