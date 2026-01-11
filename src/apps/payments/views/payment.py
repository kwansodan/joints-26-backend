from src.services.payments import *
from src.utils.helpers import BaseAPIView
from src.apps.payments.permissions import PaymentModelPermission 

class PaymentListView(BaseAPIView):
    permission_classes = [PaymentModelPermission]

    def get(self, request):
        success, message, data = paymentListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createPaymentService(request.data)
        return self.created(message, data) if success else self.bad(message)

class PaymentDetailView(BaseAPIView):
    permission_classes = [PaymentModelPermission]

    def get(self, request, pk):
        success, message, data = getPaymentDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updatePaymentDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updatePaymentDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deletePaymentService(pk)
        return self.ok(message, data) if success else self.bad(message)

