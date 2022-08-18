from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# TokenObtain == Access Token 으로 생각하면 됨! 
# 즉, 이곳에서 claim에 어떤 정보를 담고 싶은지에 대한 커스터마이징을 진행하면 됨!
class SeasonTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    # database에서 조회된 user의 정보가 user로 들어오게 된다. (요청한 user의 정보)
    def get_token(cls, user):
		# 가지고 온 user의 정보를 바탕으로 token을 생성한다.
        token = super().get_token(user)

        # 로그인한 사용자의 클레임 설정하기.
        token["id"] = user.id
        token["username"] = user.username
        token["email"] = user.email

        return token