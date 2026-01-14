from src.services.vehicles import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.bikers.permissions import VehicleModelPermission

class VehicleListView(BaseAPIView, GenericAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [VehicleModelPermission]

    def get(self, request):
        success, message, data = vehiclesListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createVehicleService(request.data)
        return self.created(message, data) if success else self.bad(message)

class VehicleDetailView(BaseAPIView, GenericAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [VehicleModelPermission]

    def get(self, request, pk):
        success, message, data = getVehicleDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateVehicleDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateVehicleDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteVehicleService(pk)
        return self.ok(message, data) if success else self.bad(message)

