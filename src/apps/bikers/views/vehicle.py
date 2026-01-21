from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from src.services.vehicles import *
from src.utils.helpers import DETAIL_VIEW_HTTP_METHODS, LIST_VIEW_HTTP_METHODS, BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.bikers.permissions import VehicleModelPermission
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400, INVALID_CREDENTIALS_401
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


@extend_schema_view(
    get=extend_schema(
        description="List all biker vehicles",
        responses={
            200: VehicleSerializer(many=True), 
            **FORBIDDEN_403,
            **BAD_REQUEST_400,
            **INVALID_CREDENTIALS_401,
        },
    ),
    post=extend_schema(
        description="Create a new biker vehicle",
        request=VehicleSerializer,
        responses={
            201: VehicleSerializer,
            **FORBIDDEN_403,
            **BAD_REQUEST_400,
            **INVALID_CREDENTIALS_401,
        }
    ),
)
class VehicleListView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = LIST_VIEW_HTTP_METHODS 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, VehicleModelPermission]
    serializer_class = VehicleSerializer

    def get(self, request):
        success, message, data = vehiclesListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createVehicleService(request.data)
        return self.created(message, data) if success else self.bad(message)


@extend_schema_view(
    get=extend_schema(
        description="Get a single biker vehicle",
        responses={
            200: VehicleSerializer, 
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    put=extend_schema(
        description="Update a single biker vehicle",
        request=VehicleSerializer,
        responses={
            200: VehicleSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
    patch=extend_schema(
        description="Partially update a single biker vehicle",
        request=VehicleSerializer,
        responses={
            200: VehicleSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
    delete=extend_schema(
        description="Delete a single biker vehicle",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
)
class VehicleDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, VehicleModelPermission]
    serializer_class = VehicleSerializer

    def get(self, request, pk):
        success, message, data = getVehicleDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateVehicleDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateVehicleDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteVehicleService(pk)
        return self.no_content() if success else self.bad(message)
 
