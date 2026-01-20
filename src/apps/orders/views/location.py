from src.services.location import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.orders.permissions import LocationModelPermission 
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


@extend_schema_view(
    get=extend_schema(
        description="List all locations",
        responses={
            200: LocationSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        },
    ),
    post=extend_schema(
        description="Create a new location",
        request=LocationSerializer,
        responses={
            201: LocationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
)
class LocationListView(BaseAPIView, GenericAPIView):
    serializer_class = LocationSerializer
    permission_classes = [LocationModelPermission]

    def get(self, request):
        success, message, data = locationListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createLocationService(request.data)
        return self.created(message, data) if success else self.bad(message)


@extend_schema_view(
    get=extend_schema(
        description="Get a single location",
        responses={
            200: LocationSerializer, 
            **FORBIDDEN_403
        },
    ),
    put=extend_schema(
        description="Update a single location",
        request=LocationSerializer,
        responses={
            200: LocationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    patch=extend_schema(
        description="Partially update a single location",
        request=LocationSerializer,
        responses={
            200: LocationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    delete=extend_schema(
        description="Delete a single location",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403
        }
    ),
)
class LocationDetailView(BaseAPIView, GenericAPIView):
    serializer_class = LocationSerializer
    permission_classes = [LocationModelPermission]

    def get(self, request, pk):
        success, message, data = getLocationDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateLocationDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateLocationDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data =deleteLocationService(pk)
        return self.ok(message, data) if success else self.bad(message)

