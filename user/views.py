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

from the_season.settings import SECRET_KEY, ALGORITHM, SIMPLE_JWT
import jwt

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
        # jwt 디코딩
        client_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        token = jwt.decode(client_token, SECRET_KEY, algorithms=ALGORITHM) 
        print(f'token: {token}')
        
        user = UserModel.objects.get(id=token["user_id"])
        user_serializer = UserSerializer(user, data=request.data, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DONE 회원 탈퇴
    def delete(self, request):
        # jwt 디코딩
        client_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        token = jwt.decode(client_token, SECRET_KEY, algorithms=ALGORITHM) 
        print(f'token: {token}')
        
        user = UserModel.objects.get(id=token["user_id"])
        if user:
            user.delete()
            return Response({"message": "회원탈퇴 성공"}, status=status.HTTP_200_OK)
        return Response({"message": "회원탈퇴 실패"}, status=status.HTTP_400_BAD_REQUEST)
    
# 인가된 사용자의 정보 조회
class OnlyAuthenticatedUserView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] # JWT 인증방식 클래스 지정하기

    def get(self, request):
        # Token에서 인증된 사용자의 정보만을 가져온다.
        client_token = request.headers.get('Authorization', None).replace('Bearer ', '')
        token = jwt.decode(client_token, SECRET_KEY, algorithms=ALGORITHM)
        
        user_info = UserModel.objects.get(id=token["user_id"])
        serialized_user = UserSerializer(user_info)
        
        if not client_token:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"user_info": serialized_user.data}, status=status.HTTP_200_OK)