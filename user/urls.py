from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user import views
from user.views import SeasonTokenObtainPairView


urlpatterns = [
    path('', views.UserView.as_view()),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
    # simplejwt 에서 제공하는 기본 JWT 인증 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/season/token/', SeasonTokenObtainPairView.as_view(), name='season_token'),
    path('api/authonly/', views.OnlyAuthenticatedUserView.as_view()),
]

