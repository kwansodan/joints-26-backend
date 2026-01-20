from src.services.order import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.orders.permissions import OrderModelPermission
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        description="List all orders",
        responses={
            200: OrderSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        },
    ),
    post=extend_schema(
        description="Create a new order",
        request=OrderSerializer,
        responses={
            201: OrderSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
)
class OrderListView(BaseAPIView, GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [OrderModelPermission]

    def get(self, request):
        success, message, data = orderListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createOrderService(request.data)
        return self.created(message, data) if success else self.bad(message)


@extend_schema_view(
    get=extend_schema(
        description="Get a single order",
        responses={
            200: OrderSerializer, 
            **FORBIDDEN_403
        },
    ),
    put=extend_schema(
        description="Update a single order",
        request=OrderSerializer,
        responses={
            200: OrderSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    patch=extend_schema(
        description="Partially update a single order",
        request=OrderSerializer,
        responses={
            200: OrderSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    delete=extend_schema(
        description="Delete a single order",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403
        }
    ),
)
class OrderDetailView(BaseAPIView, GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [OrderModelPermission]

    def get(self, request, pk):
        success, message, data = getOrderDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateOrderDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateOrderDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteOrderService(pk)
        return self.ok(message, data) if success else self.bad(message)

