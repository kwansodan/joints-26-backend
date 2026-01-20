from src.services.order_item import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.orders.permissions import OrderItemModelPermission
from src.utils.helpers import BaseAPIView, FORBIDDEN_403, BAD_REQUEST_400
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        description="List all orderitems",
        responses={
            200: OrderItemSerializer(many=True), 
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        },
    ),
    post=extend_schema(
        description="Create a new orderitem",
        request=OrderItemSerializer,
        responses={
            201: OrderItemSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
)
class OrderItemListView(BaseAPIView, GenericAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [OrderItemModelPermission]

    def get(self, request):
        success, message, data = orderItemListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createOrderItemService(request.data)
        return self.created(message, data) if success else self.bad(message)

@extend_schema_view(
    get=extend_schema(
        description="Get a single orderitem",
        responses={
            200: OrderItemSerializer, 
            **FORBIDDEN_403
        },
    ),
    put=extend_schema(
        description="Update a single orderitem",
        request=OrderItemSerializer,
        responses={
            200: OrderItemSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    patch=extend_schema(
        description="Partially update a single orderitem",
        request=OrderItemSerializer,
        responses={
            200: OrderItemSerializer,
            **BAD_REQUEST_400,
            **FORBIDDEN_403
        }
    ),
    delete=extend_schema(
        description="Delete a single orderitem",
        responses={
            204: OpenApiResponse(description="Deleted successfully"),
            **FORBIDDEN_403
        }
    ),
)
class OrderItemDetailView(BaseAPIView, GenericAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [OrderItemModelPermission]

    def get(self, request, pk):
        success, message, data = getOrderItemDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateOrderItemDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateOrderItemDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteOrderItemService(pk)
        return self.ok(message, data) if success else self.bad(message)

