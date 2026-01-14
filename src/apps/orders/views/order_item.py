from src.services.order_item import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.orders.permissions import OrderItemModelPermission

class OrderItemListView(BaseAPIView, GenericAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [OrderItemModelPermission]

    def get(self, request):
        success, message, data = orderItemListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createOrderItemService(request.data)
        return self.created(message, data) if success else self.bad(message)

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

