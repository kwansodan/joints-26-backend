from src.services.users import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.users.permissions import UserModelPermission
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        description="List all users",
        responses={
            200: AuthSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        },
    ),
    post=extend_schema(
        description="Create a new user",
        request=AuthSerializer,
        responses={
            201: AuthSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
)
class UserListView(BaseAPIView, GenericAPIView):
    serializer_class = AuthSerializer 
    permission_classes = [UserModelPermission]

    def get(self, request):
        success, message, data = usersListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createUserService(request.data)
        return self.created(message, data) if success else self.bad(message)

@extend_schema_view(
    get=extend_schema(
        description="Get a single user",
        responses={
            200: AuthSerializer, 
            **FORBIDDEN_403
        },
    ),
    put=extend_schema(
        description="Update a single user",
        request=AuthSerializer,
        responses={
            200: AuthSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    patch=extend_schema(
        description="Partially update a single user",
        request=AuthSerializer,
        responses={
            200: AuthSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    delete=extend_schema(
        description="Delete a single user",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403
        }
    ),
)
class UserDetailView(BaseAPIView, GenericAPIView):
    serializer_class = AuthSerializer 
    permission_classes = [UserModelPermission]

    def get(self, request, pk):
        success, message, data = getUserDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateUserService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateUserService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteUserService(pk)
        return self.ok(message, data) if success else self.bad(message)

