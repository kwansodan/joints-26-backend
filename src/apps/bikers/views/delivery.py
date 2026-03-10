from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from src.apps.bikers.permissions import DeliveryModelPermission
from src.apps.bikers.serializers import DeliverySerializer
from src.services.delivery import *
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
        description="List all deliveries",
        responses={
            200: DeliverySerializer(many=True),
            **FORBIDDEN_403,
            **BAD_REQUEST_400,
            **INVALID_CREDENTIALS_401,
        },
    ),
    post=extend_schema(
        description="Create a new delivery",
        request=DeliverySerializer,
        responses={
            201: DeliverySerializer,
            **FORBIDDEN_403,
            **BAD_REQUEST_400,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class DeliveryListView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = LIST_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, DeliveryModelPermission]
    serializer_class = DeliverySerializer

    def get(self, request):
        success, message, data = deliveryListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createDeliveryService(requestData=request.data)
        return self.created(message, data) if success else self.bad(message)


@extend_schema_view(
    get=extend_schema(
        description="Get a single delivery",
        responses={
            200: DeliverySerializer,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    put=extend_schema(
        description="Update a single delivery",
        request=DeliverySerializer,
        responses={
            200: DeliverySerializer,
            **FORBIDDEN_403,
            **BAD_REQUEST_400,
            **INVALID_CREDENTIALS_401,
        },
    ),
    patch=extend_schema(
        description="Partially update a single delivery",
        request=DeliverySerializer,
        responses={
            200: DeliverySerializer,
            **FORBIDDEN_403,
            **BAD_REQUEST_400,
            **INVALID_CREDENTIALS_401,
        },
    ),
    delete=extend_schema(
        description="Delete a single delivery",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class DeliveryDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, DeliveryModelPermission]
    serializer_class = DeliverySerializer

    def get(self, request, pk):
        success, message, data = getDeliveryDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateDeliveryDetailService(
            pk=pk, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateDeliveryDetailService(
            pk=pk, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, _ = deleteDeliveryDetailService(pk)
        return self.no_content() if success else self.bad(message)
