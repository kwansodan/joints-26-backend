from src.services.vendors import *
from src.utils.helpers import BaseAPIView
from src.apps.vendors.permissions import VendorModelPermission 

class VendorListView(BaseAPIView):
    permission_classes = [VendorModelPermission]

    def get(self, request):
        success, message, data = vendorsListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createVendorService(requestData=request.data)
        return self.created(message, data) if success else self.bad(message)

class VendorDetailView(BaseAPIView):
    permission_classes = [VendorModelPermission]

    def get(self, request, pk):
        success, message, data = getVendorDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateVendorDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateVendorDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteVendorService(pk)
        return self.ok(message, data) if success else self.bad(message)

