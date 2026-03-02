from django.contrib.auth import authenticate
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from src.apps.users.serializers import LoginRequestSerializer, RefreshRequestSerializer
from src.services.users import *
from src.utils.helpers import (
    BAD_REQUEST_400,
    INVALID_CREDENTIALS_401,
    SUCCESS_REQUEST_200,
    BaseAPIView,
)


@extend_schema_view(
    post=(
        extend_schema(
            description="Login",
            request=LoginRequestSerializer,
            responses={
                **SUCCESS_REQUEST_200,
                **BAD_REQUEST_400,
                **INVALID_CREDENTIALS_401,
            },
        ),
    )
)
class LoginView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = ["post"]
    serializer_class = LoginRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.data
        if not "email" in payload or not "password" in payload:
            return self.bad("Invalid payload")

        try:
            user = authenticate(
                request, username=payload["email"], password=payload["password"]
            )
            if user is not None:
                if not user.is_active:
                    return self.forbidden("User is not active")

                refresh = RefreshToken.for_user(user)
                data = {
                    "user_id": getattr(user, "id"),
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return self.ok("Login success", data=data)
            else:
                return self.unauthorized("Invalid credentials")
        except Exception as e:
            print(f"Login view exception: {str(e)}")


class RefreshTokenView(TokenRefreshView):
    parser_classes = [JSONParser]

    @extend_schema(
        request=RefreshRequestSerializer,
        responses={
            200: OpenApiResponse(description="Authentication tokens"),
            400: OpenApiResponse(description="Missing refresh token"),
            401: OpenApiResponse(description="Invalid or expired token"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
