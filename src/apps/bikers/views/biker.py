from src.services.bikers import *
from rest_framework.generics import GenericAPIView
from src.apps.bikers.permissions import BikerModelPermission
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        description="List all bikers",
        responses={
            200: BikerSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        },
    ),
    post=extend_schema(
        description="Create a new biker",
        request=BikerSerializer,
        responses={
            201: BikerSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
)
class BikerListView(BaseAPIView, GenericAPIView):
    serializer_class = BikerSerializer 
    permission_classes = [BikerModelPermission]

    def get(self, request):
        success, message, data = bikersListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createBikerService(request.data)
        return self.created(message, data) if success else self.bad(message)


@extend_schema_view(
    get=extend_schema(
        description="Get a single biker",
        responses={
            200: BikerSerializer, 
            **FORBIDDEN_403
        },
    ),
    put=extend_schema(
        description="Update a single biker",
        request=BikerSerializer,
        responses={
            200: BikerSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    patch=extend_schema(
        description="Partially update a single biker",
        request=BikerSerializer,
        responses={
            200: BikerSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    delete=extend_schema(
        description="Delete a single biker",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403
        }
    ),
)
class BikerDetailView(BaseAPIView, GenericAPIView):
    serializer_class = BikerSerializer 
    permission_classes = [BikerModelPermission]

    def get(self, request, pk):
        success, message, data = getBikerDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateBikerDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateBikerDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, _ = deleteBikerService(pk)
        return self.no_content() if success else self.bad(message)

