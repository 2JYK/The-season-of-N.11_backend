from rest_framework import serializers
from .models import User as UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["username", "password", "email", "fullname", "join_date"]
        
        extra_kwargs = {
            'password': {'write_only': True},
        }