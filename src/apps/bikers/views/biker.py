from src.services.bikers import *
from rest_framework.parsers import JSONParser
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from src.apps.bikers.permissions import BikerModelPermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from src.utils.helpers import BaseAPIView, INVALID_CREDENTIALS_401, BAD_REQUEST_400, FORBIDDEN_403, LIST_VIEW_HTTP_METHODS, DETAIL_VIEW_HTTP_METHODS

@extend_schema_view(
    get=extend_schema(
        description="List all bikers",
        responses={
            200: BikerSerializer(many=True), 
            **FORBIDDEN_403,
            **BAD_REQUEST_400,
            **INVALID_CREDENTIALS_401,
        },
    ),
    post=extend_schema(
        description="Create a new biker",
        request=BikerSerializer,
        responses={
            201: BikerSerializer,
            **FORBIDDEN_403,
            **BAD_REQUEST_400,
            **INVALID_CREDENTIALS_401,
        }
    ),
)
class BikerListView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = LIST_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BikerModelPermission]
    serializer_class = BikerSerializer 

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
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    put=extend_schema(
        description="Update a single biker",
        request=BikerSerializer,
        responses={
            200: BikerSerializer,
            **FORBIDDEN_403,
            **BAD_REQUEST_400,
            **INVALID_CREDENTIALS_401,

        }
    ),
    patch=extend_schema(
        description="Partially update a single biker",
        request=BikerSerializer,
        responses={
            200: BikerSerializer,
            **FORBIDDEN_403,
            **BAD_REQUEST_400,
            **INVALID_CREDENTIALS_401,
        }
    ),
    delete=extend_schema(
        description="Delete a single biker",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
)
class BikerDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, BikerModelPermission]
    serializer_class = BikerSerializer 


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

