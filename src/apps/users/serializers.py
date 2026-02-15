from rest_framework import serializers

from src.apps.users.models import Customer, User


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=1)
    password = serializers.RegexField(
        regex=r"^[^\x00]+$", min_length=1, write_only=True
    )


class RefreshRequestSerializer(serializers.Serializer):
    refresh = serializers.RegexField(regex=r"^[^\x00]+$", min_length=1, write_only=True)


class AuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

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


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
        ]
