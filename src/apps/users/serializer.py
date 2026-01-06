from src.apps.users.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class AuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # user_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User 
        fields = [
              "id",
              "first_name",
              "last_name",
              "email", 
              "phone",
              "password",
              "userType",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password) 
        user.save()
        return user

    def get_user_type(self, obj):
        if not hasattr(obj, "id"):
            return None
        return getattr(obj, "userType", "regular") 


