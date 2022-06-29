from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

from user.models import User as UserModel
from user.serializers import UserSerializer

from rest_framework.permissions import IsAuthenticated

from user.jwt_claim_serializer import SeasonTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

# TokenObtainPairView : urls.py에서 import했고, 토큰을 발급받기 위해 사용
class SeasonTokenObtainPairView(TokenObtainPairView):
    # serializer_class에 커스터마이징된 시리얼라이저를 넣어 준다.
    serializer_class = SeasonTokenObtainPairSerializer

class UserView(APIView):
    
    # DONE 회원 정보 조회
    def get(self, request):
        data = UserModel.objects.get(id=request.user.id)
        return Response(UserSerializer(data).data, status=status.HTTP_200_OK)

    # DONE 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DONE 회원 정보 수정
    def put(self, request):
        user = UserModel.objects.get(id=request.user.id)
        user_serializer = UserSerializer(user, data=request.data, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DONE 회원 탈퇴
    def delete(self, request):
        user = UserModel.objects.get(id=request.user.id)
        if user:
            user.delete()
            return Response({"message": "회원탈퇴 성공"}, status=status.HTTP_200_OK)
        return Response({"message": "회원탈퇴 실패"}, status=status.HTTP_400_BAD_REQUEST)
   
class UserAPIView(APIView):
    
    # DONE 로그인
    # def post(self, request):
    #     username = request.data.get('username', '')
    #     password = request.data.get('password', '')
        
    #     user = authenticate(request, username=username, password=password)
        
    #     if not user:
    #         return Response({"msg": "존재하지 않는 계정이거나 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
    #     login(request, user)
        
    #     return Response({"msg": "로그인 성공!!"}, status=status.HTTP_200_OK)
    
    # DONE 로그아웃
    def delete(self, request):
        logout(request)
        return Response({"msg": "로그아웃 성공!!"}, status=status.HTTP_200_OK)
    
    
# 인가된 사용자만 접근할 수 있는 View 생성
class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
		
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # Token에서 인증된 user만 가져온다.
        user = request.user
        print(f"user 정보 : {user}")
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message": "Accepted"})