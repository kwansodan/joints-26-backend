from src.services.payments import *
from src.utils.helpers import DETAIL_VIEW_HTTP_METHODS, INVALID_CREDENTIALS_401, LIST_VIEW_HTTP_METHODS, BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.payments.permissions import PaymentModelPermission 
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


@extend_schema_view(
    get=extend_schema(
        description="List all payments",
        responses={
            200: PaymentSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401
        },
    ),
    post=extend_schema(
        description="Create a new payment",
        request=PaymentSerializer,
        responses={
            201: PaymentSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401
        }
    ),
)
class PaymentListView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = LIST_VIEW_HTTP_METHODS 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PaymentModelPermission]
    serializer_class = PaymentSerializer

    def get(self, request):
        success, message, data = paymentListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createPaymentService(request.data)
        return self.created(message, data) if success else self.bad(message)

@extend_schema_view(
    get=extend_schema(
        description="Get a single payment",
        responses={
            200: PaymentSerializer, 
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401
        },
    ),
    put=extend_schema(
        description="Update a single payment",
        request=PaymentSerializer,
        responses={
            200: PaymentSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401
        }
    ),
    patch=extend_schema(
        description="Partially update a single payment",
        request=PaymentSerializer,
        responses={
            200: PaymentSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401
        }
    ),
    delete=extend_schema(
        description="Delete a single payment",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401
        }
    ),
)
class PaymentDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, PaymentModelPermission]
    serializer_class = PaymentSerializer

    def get(self, request, pk):
        success, message, data = getPaymentDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updatePaymentDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updatePaymentDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deletePaymentService(pk)
        return self.no_content() if success else self.bad(message)

