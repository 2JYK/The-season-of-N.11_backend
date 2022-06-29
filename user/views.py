from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

# from user.serializers import UserSerializer
   
class UserAPIView(APIView):
    
    # DONE 로그인
    def post(self, request):
        username = request.post.get('username', '')
        password = request.post.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        
        if not user:
            return Response({"msg": "존재하지 않는 계정이거나 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        login(request, user)
        
        return Response({"msg": "로그인 성공!!"}, status=status.HTTP_200_OK)
    
    # DONE 로그아웃
    def delete(self, request):
        logout(request)
        return Response("msg": "로그아웃 성공!!", status=status.HTTP_200_OK)