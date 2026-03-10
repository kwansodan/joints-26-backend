from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from src.apps.vendors.permissions import VendorRedeemTokenModelPermission
from src.apps.vendors.serializers import VendorRedeemTokenSerializer
from src.services.vendor_redeem_token import *
from src.services.vendors import *
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
        description="List all vendors redeem tokens",
        responses={
            200: VendorRedeemTokenSerializer(many=True),
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    post=extend_schema(
        description="Create a new vendor redeem token",
        request=VendorRedeemTokenSerializer,
        responses={
            201: VendorRedeemTokenSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class VendorRedeemTokenListView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = LIST_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, VendorRedeemTokenModelPermission]
    serializer_class = VendorRedeemTokenSerializer

    def get(self, request):
        success, message, data = vendorRedeemTokenListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createVendorService(requestData=request.data)
        return self.created(message, data) if success else self.bad(message)


@extend_schema_view(
    get=extend_schema(
        description="Get a single vendor redeem token",
        responses={
            200: VendorRedeemTokenSerializer,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    put=extend_schema(
        description="Update a single vendor redeem token",
        request=VendorRedeemTokenSerializer,
        responses={
            200: VendorRedeemTokenSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    patch=extend_schema(
        description="Partially update a single vendor redeem token",
        request=VendorRedeemTokenSerializer,
        responses={
            200: VendorRedeemTokenSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    delete=extend_schema(
        description="Delete a single vendor redeem token",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class VendorRedeemTokenDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, VendorRedeemTokenModelPermission]
    serializer_class = VendorRedeemTokenSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [permission() for permission in self.permission_classes]

    def get(self, request, pk):
        success, message, data = getVendorRedeemTokenDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateVendorRedeemTokenDetailService(
            pk=pk, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateVendorRedeemTokenDetailService(
            pk=pk, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteVendorRedeemTokenService(pk)
        return self.no_content() if success else self.bad(message)
