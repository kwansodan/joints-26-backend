from src.services.vendors import *
from src.utils.helpers import DETAIL_VIEW_HTTP_METHODS, LIST_VIEW_HTTP_METHODS, BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.vendors.permissions import VendorModelPermission 
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400, INVALID_CREDENTIALS_401
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


@extend_schema_view(
    get=extend_schema(
        description="List all vendors",
        responses={
            200: VendorSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    post=extend_schema(
        description="Create a new vendor",
        request=VendorSerializer,
        responses={
            201: VendorSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
)
class VendorListView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = LIST_VIEW_HTTP_METHODS 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, VendorModelPermission]
    serializer_class = VendorSerializer

    def get(self, request):
        success, message, data = vendorsListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createVendorService(requestData=request.data)
        return self.created(message, data) if success else self.bad(message)


@extend_schema_view(
    get=extend_schema(
        description="Get a single vendor",
        responses={
            200: VendorSerializer, 
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    put=extend_schema(
        description="Update a single vendor",
        request=VendorSerializer,
        responses={
            200: VendorSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
    patch=extend_schema(
        description="Partially update a single vendor",
        request=VendorSerializer,
        responses={
            200: VendorSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
    delete=extend_schema(
        description="Delete a single vendor",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
)
class VendorDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, VendorModelPermission]
    serializer_class = VendorSerializer

    def get(self, request, pk):
        success, message, data = getVendorDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateVendorDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateVendorDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteVendorService(pk)
        return self.no_content() if success else self.bad(message)

