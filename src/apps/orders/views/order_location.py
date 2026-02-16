from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from src.apps.orders.permissions import OrderLocationModelPermission
from src.apps.orders.serializers import OrderLocationSerializer
from src.services.order_location import *
from src.utils.helpers import (
    BAD_REQUEST_400,
    DETAIL_VIEW_HTTP_METHODS,
    FORBIDDEN_403,
    INVALID_CREDENTIALS_401,
    LIST_VIEW_HTTP_METHODS,
    BaseAPIView,
)


@extend_schema_view(
    get=extend_schema(
        description="List all order locations",
        responses={
            200: OrderLocationSerializer(many=True),
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    post=extend_schema(
        description="Create a new order location",
        request=OrderLocationSerializer,
        responses={
            201: OrderLocationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class OrderLocationListView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = LIST_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OrderLocationModelPermission]
    serializer_class = OrderLocationSerializer
    permission_classes = [OrderLocationModelPermission]

    def get(self, request):
        success, message, data = orderLocationListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createOrderLocationService(request.data)
        return self.created(message, data) if success else self.bad(message)


@extend_schema_view(
    get=extend_schema(
        description="Get a single order location",
        responses={
            200: OrderLocationSerializer,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    put=extend_schema(
        description="Update a single order location",
        request=OrderLocationSerializer,
        responses={
            200: OrderLocationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    patch=extend_schema(
        description="Partially update a order single location",
        request=OrderLocationSerializer,
        responses={
            200: OrderLocationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    delete=extend_schema(
        description="Delete a single order location",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class OrderLocationDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OrderLocationModelPermission]
    serializer_class = OrderLocationSerializer
    permission_classes = [OrderLocationModelPermission]

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "PATCH"]:
            return [AllowAny()]
        return [permission() for permission in self.permission_classes]

    def get(self, request, token, order_location_id):
        success, message, data = getOrderLocationDetailService(
            token=token, order_location_id=order_location_id
        )
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, token, order_location_id):
        success, message, data = updateOrderLocationDetailService(
            token=token, order_location_id=order_location_id, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, token, order_location_id):
        success, message, data = updateOrderLocationDetailService(
            token=token, order_location_id=order_location_id, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteOrderLocationService(pk)
        return self.no_content() if success else self.bad(message)
