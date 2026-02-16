from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from src.apps.orders.permissions import OrderItemModelPermission
from src.apps.payments.serializers import PaymentSerializer
from src.services.order_item import *
from src.services.order_payments import updateCustomerOrderPayment
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
        description="Update order payment",
        request=OpenApiResponse,
        responses={
            **SUCCESS_REQUEST_200,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    patch=extend_schema(
        description="Partially update order payment",
        request=OpenApiResponse,
        responses={
            **SUCCESS_REQUEST_200,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class PaystackUpdateOrderPaymentDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OrderItemModelPermission]
    serializer_class = OrderItemSerializer

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "PATCH"]:
            return [AllowAny()]
        return [permission() for permission in self.permission_classes]

    def put(self, request, pk):
        success, message, data = updateCustomerOrderPayment(
            pk=pk, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateCustomerOrderPayment(
            pk=pk, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)
