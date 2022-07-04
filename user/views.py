from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from user.serializers import UserSerializer

from user.jwt_claim_serializer import SeasonTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


# 토큰을 발급용 #
class SeasonTokenObtainPairView(TokenObtainPairView):
    serializer_class = SeasonTokenObtainPairSerializer

        
class UserView(APIView):
    authentication_classes = [JWTAuthentication] 
     
    # 회원 정보 조회 #
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    # 회원가입 #
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원 정보 수정 #
    def put(self, request):
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원 탈퇴 #
    def delete(self, request):
        user = request.user
        
        if user:
            user.delete()
            return Response({"message": "회원탈퇴 성공"}, status=status.HTTP_200_OK)
        
        return Response({"message": "회원탈퇴 실패"}, status=status.HTTP_400_BAD_REQUEST)
    
    
class OnlyAuthenticatedUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication] 
    
    # 인가된 사용자의 정보 조회 #
    def get(self, request):
        user = request.user
        
        if not user:
            return Response({"error": "접근 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serialized_user = UserSerializer(user)
        return Response({"user_info": serialized_user.data}, status=status.HTTP_200_OK)
    
