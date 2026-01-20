from src.services.vendors import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.vendors.permissions import VendorModelPermission 
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        description="List all vendors",
        responses={
            200: VendorSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        },
    ),
    post=extend_schema(
        description="Create a new vendor",
        request=VendorSerializer,
        responses={
            201: VendorSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
)
class VendorListView(BaseAPIView, GenericAPIView):
    serializer_class = VendorSerializer
    permission_classes = [VendorModelPermission]

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
            **FORBIDDEN_403
        },
    ),
    put=extend_schema(
        description="Update a single vendor",
        request=VendorSerializer,
        responses={
            200: VendorSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    patch=extend_schema(
        description="Partially update a single vendor",
        request=VendorSerializer,
        responses={
            200: VendorSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    delete=extend_schema(
        description="Delete a single vendor",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403
        }
    ),
)
class VendorDetailView(BaseAPIView, GenericAPIView):
    serializer_class = VendorSerializer
    permission_classes = [VendorModelPermission]

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
        return self.ok(message, data) if success else self.bad(message)

