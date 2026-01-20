from src.services.notifications import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.notifications.permissions import NotificationModelPermission
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        description="List all notifications",
        responses={
            200: NotificationSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        },
    ),
    post=extend_schema(
        description="Create a new notification",
        request=NotificationSerializer,
        responses={
            201: NotificationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
)
class NotificationListView(BaseAPIView, GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [NotificationModelPermission]

    def get(self, request):
        success, message, data = notificationListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createNotificationService(request.data)
        return self.created(message, data) if success else self.bad(message)

@extend_schema_view(
    get=extend_schema(
        description="Get a single notification",
        responses={
            200: NotificationSerializer, 
            **FORBIDDEN_403
        },
    ),
    put=extend_schema(
        description="Update a single notification",
        request=NotificationSerializer,
        responses={
            200: NotificationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    patch=extend_schema(
        description="Partially update a single notification",
        request=NotificationSerializer,
        responses={
            200: NotificationSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    delete=extend_schema(
        description="Delete a single notification",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403
        }
    ),
)
class NotificationDetailView(BaseAPIView, GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [NotificationModelPermission]

    def get(self, request, pk):
        success, message, data = getNotificationDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateNotificationDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateNotificationDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteNotificationService(pk)
        return self.ok(message, data) if success else self.bad(message)

