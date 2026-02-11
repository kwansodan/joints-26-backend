from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from src.apps.orders.permissions import OrderItemModelPermission
from src.services.order_item import *
from src.services.wegoo import updateOrderRiderDispatch
from src.utils.helpers import (
    BAD_REQUEST_400,
    DETAIL_VIEW_HTTP_METHODS,
    FORBIDDEN_403,
    INVALID_CREDENTIALS_401,
    SUCCESS_REQUEST_200,
    BaseAPIView,
)


@extend_schema_view(
    put=extend_schema(
        description="Update order rider dispatch",
        request=OpenApiResponse,
        responses={
            **SUCCESS_REQUEST_200,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    patch=extend_schema(
        description="Partially update order rider dispatch",
        request=OpenApiResponse,
        responses={
            **SUCCESS_REQUEST_200,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class WegooDispatchDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OrderItemModelPermission]
    serializer_class = OrderItemSerializer

    def put(self, request, pk):
        success, message, data = updateOrderRiderDispatch(
            pk=pk, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateOrderRiderDispatch(
            pk=pk, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)
