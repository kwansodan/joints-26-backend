from src.services.bikers import *
from src.utils.helpers import BaseAPIView
from rest_framework.generics import GenericAPIView
from src.apps.bikers.permissions import BikerModelPermission

class BikerListView(BaseAPIView, GenericAPIView):
    serializer_class = BikerSerializer 
    permission_classes = [BikerModelPermission]

    def get(self, request):
        success, message, data = bikersListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createBikerService(request.data)
        return self.created(message, data) if success else self.bad(message)

class BikerDetailView(BaseAPIView, GenericAPIView):
    serializer_class = BikerSerializer 
    permission_classes = [BikerModelPermission]

    def get(self, request, pk):
        success, message, data = getBikerDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateBikerDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateBikerDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteBikerService(pk)
        return self.ok(message, data) if success else self.bad(message)

