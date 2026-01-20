from src.services.payments import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.payments.permissions import PaymentModelPermission 
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        description="List all payments",
        responses={
            200: PaymentSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        },
    ),
    post=extend_schema(
        description="Create a new payment",
        request=PaymentSerializer,
        responses={
            201: PaymentSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
)
class PaymentListView(BaseAPIView, GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [PaymentModelPermission]

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
            **FORBIDDEN_403
        },
    ),
    put=extend_schema(
        description="Update a single payment",
        request=PaymentSerializer,
        responses={
            200: PaymentSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    patch=extend_schema(
        description="Partially update a single payment",
        request=PaymentSerializer,
        responses={
            200: PaymentSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    delete=extend_schema(
        description="Delete a single payment",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403
        }
    ),
)
class PaymentDetailView(BaseAPIView, GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [PaymentModelPermission]

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
        return self.ok(message, data) if success else self.bad(message)

