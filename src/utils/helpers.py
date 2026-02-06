from secrets import token_urlsafe
from rest_framework import status
from rest_framework.views import APIView
from src.utils.dbOptions import TOKEN_LEN
from rest_framework.test import APITestCase 
from rest_framework.response import Response
from drf_spectacular.utils import OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken

# spectral linter helpers
BAD_REQUEST_400 = {
    400: OpenApiResponse(description="Bad Request")
}

INVALID_CREDENTIALS_401 = {
    401: OpenApiResponse(description="Invalid credentials")
}

FORBIDDEN_403 = {
    403: OpenApiResponse(description="Forbidden")
}

LIST_VIEW_HTTP_METHODS = ["get", "post"]

DETAIL_VIEW_HTTP_METHODS = ["get", "put", "patch", "delete"]

class AllowOnlyMethodsMixin:
    def initial(self, request, *args, **kwargs):
        if request.method.lower() not in getattr(self, "http_method_names", []):
            return Response(
                {"detail": f"Method '{request.method}' not allowed."},
                status=405,
            )
        return super().initial(request, *args, **kwargs)

class BaseAPIView(AllowOnlyMethodsMixin, APIView):
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

def clean_db_error_msgs(data: str):
    print("actul error", data)
    if data.startswith("duplicate key value violates unique constraint"):
        newdata = data.splitlines()[0].split("constraint")[1].split("_")
        return f"{str(newdata[len(newdata)-2]).capitalize()} already exists"
    else:
        return data

