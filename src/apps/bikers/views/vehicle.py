from src.services.vehicles import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.bikers.permissions import VehicleModelPermission
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


@extend_schema_view(
    get=extend_schema(
        description="List all biker vehicles",
        responses={
            200: VehicleSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        },
    ),
    post=extend_schema(
        description="Create a new biker vehicle",
        request=VehicleSerializer,
        responses={
            201: VehicleSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
)
class VehicleListView(BaseAPIView, GenericAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [VehicleModelPermission]

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
            **FORBIDDEN_403
        },
    ),
    put=extend_schema(
        description="Update a single biker vehicle",
        request=VehicleSerializer,
        responses={
            200: VehicleSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    patch=extend_schema(
        description="Partially update a single biker vehicle",
        request=VehicleSerializer,
        responses={
            200: VehicleSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    delete=extend_schema(
        description="Delete a single biker vehicle",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403
        }
    ),
)
class VehicleDetailView(BaseAPIView, GenericAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [VehicleModelPermission]

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
        return self.ok(message, data) if success else self.bad(message)
 
