from src.services.menu import * 
from src.utils.helpers import BaseAPIView
from src.apps.vendors.permissions import MenuItemModelPermission 

class MenuListView(BaseAPIView):
    permission_classes = [MenuItemModelPermission]

    def get(self, request):
        success, message, data = menuListService()
        return self.ok(message, data) if success else self.bad(message)

    def post(self, request):
        success, message, data = createMenuService(request.data)
        return self.created(message, data) if success else self.bad(message)

class MenuDetailView(BaseAPIView):
    permission_classes = [MenuItemModelPermission]

    def get(self, request, pk):
        success, message, data = getMenuDetailService(pk=pk)
        return self.ok(message, data) if success else self.bad(message)

    def put(self, request, pk):
        success, message, data = updateMenuDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def patch(self, request, pk):
        success, message, data = updateMenuDetailService(pk=pk, requestData=request.data)
        return self.ok(message, data) if success else self.bad(message)

    def delete(self, request, pk):
        success, message, data = deleteMenuService(pk)
        return self.ok(message, data) if success else self.bad(message)

