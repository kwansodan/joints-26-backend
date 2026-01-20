from src.services.users import *
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiRequest
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class LoginView(TokenObtainPairView):
    @extend_schema(
    request=OpenApiRequest(
        {
            "type": "object",
            "required": True,
            "properties": {
                "email": {
                    "type": "string",
                    "format": "email",
                    "minLength": 1,
                },
                "password": {
                    "type": "string",
                    "minLength": 1,
                },
            },
            "required": ["email", "password"],
        },
        ),
        responses={
            200: OpenApiResponse(description="Authentication tokens"),
            400: OpenApiResponse(description="Invalid input"),
            401: OpenApiResponse(description="Invalid credentials"),
        },
        )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RefreshTokenView(TokenRefreshView):
    @extend_schema(
        request=OpenApiRequest(
            {
            "required": True,
            "type": "object",
                "properties": {
                    "refresh": {
                        "type": "string", 
                        "minLength": 1,
                    },
                },
                "required": ["refresh"]
            },
        ),
        responses={
            200: OpenApiResponse(description="Authentication tokens"),
            400: OpenApiResponse(description="Missing refresh token"),
            401: OpenApiResponse(description="Invalid or expired token"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


