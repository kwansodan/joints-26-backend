from src.services.location import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.orders.permissions import LocationModelPermission 

class LocationListView(BaseAPIView, GenericAPIView):
    serializer_class = LocationSerializer
    permission_classes = [LocationModelPermission]

    def get(self, request):
        success, message, data = locationListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createLocationService(request.data)
        return self.created(message, data) if success else self.bad(message)

class LocationDetailView(BaseAPIView, GenericAPIView):
    serializer_class = LocationSerializer
    permission_classes = [LocationModelPermission]

    def get(self, request, pk):
        success, message, data = getLocationDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateLocationDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateLocationDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data =deleteLocationService(pk)
        return self.ok(message, data) if success else self.bad(message)

