from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from src.apps.users.serializers import CustomerSerializer
from src.services.customers import createCustomerService, customerListService, deleteCustomerService, getCustomerDetailService, updateCustomerDetailService
from src.services.users import *
from src.utils.helpers import DETAIL_VIEW_HTTP_METHODS, INVALID_CREDENTIALS_401, LIST_VIEW_HTTP_METHODS, BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.users.permissions import CustomerModelPermission 
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        description="List all customers",
        responses={
            200: CustomerSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    post=extend_schema(
        description="Create a new customer",
        request=CustomerSerializer,
        responses={
            201: CustomerSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
)
class CustomerListView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = LIST_VIEW_HTTP_METHODS 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomerModelPermission]
    serializer_class = CustomerSerializer 

    def get(self, request):
        success, message, data = customerListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createCustomerService(request.data)
        return self.created(message, data) if success else self.bad(message)

@extend_schema_view(
    get=extend_schema(
        description="Get a single customer",
        responses={
            200: CustomerSerializer, 
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    put=extend_schema(
        description="Update a single customer",
        request=CustomerSerializer,
        responses={
            200: CustomerSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
    patch=extend_schema(
        description="Partially update a single customer",
        request=CustomerSerializer,
        responses={
            200: CustomerSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
    delete=extend_schema(
        description="Delete a single user",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        }
    ),
)
class CustomerDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CustomerModelPermission]
    serializer_class = CustomerSerializer 

    def get(self, request, pk):
        success, message, data = getCustomerDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateCustomerDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateCustomerDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, _ = deleteCustomerService(pk)
        return self.no_content() if success else self.bad(message)

