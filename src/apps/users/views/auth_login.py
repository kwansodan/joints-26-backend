from src.services.users import *
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema, OpenApiResponse 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from src.apps.users.serializers import LoginRequestSerializer, RefreshRequestSerializer

class LoginView(TokenObtainPairView):
    parser_classes = [JSONParser]

    @extend_schema(
        request=LoginRequestSerializer,
        responses={
            200: OpenApiResponse(description="Authentication tokens"),
            400: OpenApiResponse(description="Invalid input"),
            401: OpenApiResponse(description="Invalid credentials"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RefreshTokenView(TokenRefreshView):
    parser_classes = [JSONParser]

    @extend_schema(
        request=RefreshRequestSerializer, 
        responses={
            200: OpenApiResponse(description="Authentication tokens"),
            400: OpenApiResponse(description="Missing refresh token"),
            401: OpenApiResponse(description="Invalid or expired token"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


