from secrets import token_urlsafe
from rest_framework import status
from rest_framework.views import APIView
from src.utils.dbOptions import TOKEN_LEN
from rest_framework.response import Response
from rest_framework.test import APITestCase 
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import OpenApiResponse
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# spectral linter helpers
FORBIDDEN_403 = {
    403: OpenApiResponse(description="Forbidden")
}

BAD_REQUEST_400 = {
    400: OpenApiResponse(description="Bad Request")
}

class BaseAPIView(APIView):
    def ok(self, message=None, data=None):
        return Response(status=status.HTTP_200_OK, data={"message": message,  "data": data})

    def created(self, message=None, data=None):
        return Response(status=status.HTTP_201_CREATED, data={"message": message,  "data": data})

    def bad(self, message=None, data=None):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": message,  "data": data})

    def no_content(self, message=None, data=None):
        return Response(status=status.HTTP_204_NO_CONTENT, data={"message": message,  "data": data})

class BaseAPITestCase(APITestCase):
    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
    def logout(self):
        self.client.credentials()

def random_token():
    data = None
    try:
        data = str(token_urlsafe(TOKEN_LEN))
    except Exception as e:
        print(f"Failed to generate random token: {str(e)}")
    return data 



