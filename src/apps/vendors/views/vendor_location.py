from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from src.apps.vendors.permissions import (
    VendorLocationModelPermission,
    VendorModelPermission,
)
from src.apps.vendors.serializers import VendorLocationSerializer
from src.services.vendor_location import (
    createVendorLocationService,
    deleteVendorLocationService,
    getVendorLocationDetailService,
    updateVendorLocationDetailService,
    vendorLocationListService,
)
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
        description="List all vendors locations",
        responses={
            200: VendorLocationSerializer(many=True),
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    post=extend_schema(
        description="Create a new vendor location",
        request=VendorLocationSerializer,
        responses={
            201: VendorLocationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class VendorLocationListView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = LIST_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, VendorLocationModelPermission]
    serializer_class = VendorLocationSerializer

    def get(self, request):
        success, message, data = vendorLocationListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createVendorLocationService(requestData=request.data)
        return self.created(message, data) if success else self.bad(message)


@extend_schema_view(
    get=extend_schema(
        description="Get a single vendor location",
        responses={
            200: VendorLocationSerializer,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    put=extend_schema(
        description="Update a single vendor location",
        request=VendorLocationSerializer,
        responses={
            200: VendorLocationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    patch=extend_schema(
        description="Partially update a single vendor location",
        request=VendorLocationSerializer,
        responses={
            200: VendorLocationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    delete=extend_schema(
        description="Delete a single vendor location",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class VendorLocationDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, VendorLocationModelPermission]
    serializer_class = VendorLocationSerializer

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "PATCH"]:
            return [AllowAny()]
        return [permission() for permission in self.permission_classes]

    def get(self, request, pk):
        success, message, data = getVendorLocationDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        link_token = request.data.get("csrf_token", "")
        success, message, data = updateVendorLocationDetailService(
            pk=pk, link_token=link_token, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        link_token = request.data.get("csrf_token", "")
        success, message, data = updateVendorLocationDetailService(
            pk=pk, link_token=link_token, requestData=request.data
        )
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteVendorLocationService(pk)
        return self.no_content() if success else self.bad(message)
