from src.services.menu import * 
from src.utils.helpers import DETAIL_VIEW_HTTP_METHODS, INVALID_CREDENTIALS_401, LIST_VIEW_HTTP_METHODS, BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.vendors.permissions import MenuItemModelPermission 
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

@extend_schema_view(
    get=extend_schema(
        description="List all menu items",
        responses={
            200: MenuItemSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    post=extend_schema(
        description="Create a new menu item",
        request=MenuItemSerializer,
        responses={
            201: MenuItemSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
)
class MenuListView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = LIST_VIEW_HTTP_METHODS 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, MenuItemModelPermission]
    serializer_class = MenuItemSerializer

    def get(self, request):
        success, message, data = menuListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createMenuService(request.data)
        return self.created(message, data) if success else self.bad(message)

@extend_schema_view(
    get=extend_schema(
        description="Get a single menu item",
        responses={
            200: MenuItemSerializer, 
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    put=extend_schema(
        description="Update a single menu item",
        request=MenuItemSerializer,
        responses={
            200: MenuItemSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
    patch=extend_schema(
        description="Partially update a single menu item",
        request=MenuItemSerializer,
        responses={
            200: MenuItemSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
    delete=extend_schema(
        description="Delete a single menu item",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
)
class MenuDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, MenuItemModelPermission]
    serializer_class = MenuItemSerializer

    def get(self, request, pk):
        success, message, data = getMenuDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateMenuDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateMenuDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteMenuService(pk)
        return self.no_content() if success else self.bad(message)

