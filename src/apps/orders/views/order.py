from src.services.order import *
from src.utils.helpers import BaseAPIView
from src.apps.orders.permissions import OrderModelPermission

class OrderListView(BaseAPIView):
    permission_classes = [OrderModelPermission]

    def get(self, request):
        success, message, data = orderListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createOrderService(request.data)
        return self.created(message, data) if success else self.bad(message)

class OrderDetailView(BaseAPIView):
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

