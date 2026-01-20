from src.services.menu import * 
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.vendors.permissions import MenuItemModelPermission 
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        description="List all menu items",
        responses={
            200: MenuItemSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        },
    ),
    post=extend_schema(
        description="Create a new menu item",
        request=MenuItemSerializer,
        responses={
            201: MenuItemSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
)
class MenuListView(BaseAPIView, GenericAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [MenuItemModelPermission]

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
            **FORBIDDEN_403
        },
    ),
    put=extend_schema(
        description="Update a single menu item",
        request=MenuItemSerializer,
        responses={
            200: MenuItemSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    patch=extend_schema(
        description="Partially update a single menu item",
        request=MenuItemSerializer,
        responses={
            200: MenuItemSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    delete=extend_schema(
        description="Delete a single menu item",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403
        }
    ),
)
class MenuDetailView(BaseAPIView, GenericAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [MenuItemModelPermission]

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
        return self.ok(message, data) if success else self.bad(message)

