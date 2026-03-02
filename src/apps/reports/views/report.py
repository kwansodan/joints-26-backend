from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from src.apps.reports.permissions import ReportModelPermission
from src.apps.reports.serializers import ReportSerializer
from src.services.menu import *
from src.services.reports import (
    createReportService,
    deleteReportService,
    getReportDetailService,
    reportssListService,
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
        description="List all reports",
        responses={
            200: ReportSerializer(many=True),
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    post=extend_schema(
        description="Create a new report",
        request=ReportSerializer,
        responses={
            201: ReportSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class ReportListView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = LIST_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, ReportModelPermission]
    serializer_class = ReportSerializer

    def get(self, request):
        success, message, data = reportssListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        user = request.user
        success, message, data = createReportService(user=user, requestData=request.data)
        return self.created(message, data) if success else self.bad(message)


@extend_schema_view(
    get=extend_schema(
        description="Get a single report",
        responses={
            200: ReportSerializer,
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
    delete=extend_schema(
        description="Delete a single menu report",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403,
            **INVALID_CREDENTIALS_401,
        },
    ),
)
class ReportDetailView(BaseAPIView, GenericAPIView):
    parser_classes = [JSONParser]
    http_method_names = DETAIL_VIEW_HTTP_METHODS
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, ReportModelPermission]
    serializer_class = ReportSerializer

    def get(self, request, pk):
        success, message, data = getReportDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteReportService(pk)
        return self.no_content() if success else self.bad(message)
