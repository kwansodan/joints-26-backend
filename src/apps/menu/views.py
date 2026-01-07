from src.utils.apiResponse import ApiResponse
from src.apps.menu.permissions import MenuModelPermission
from rest_framework.decorators import api_view, permission_classes
from src.services.menu import *

@api_view(["GET", "POST"])
@permission_classes([MenuModelPermission])
def menuView(request):
    if request.method == "GET":
        success, message, data = menuListService() 
        if success:
            return ApiResponse("ok", message, data).response
        return ApiResponse("bad", message, data).response

    if request.method == "POST":
        success, message, data = createMenuService(requestData=request.data)
        if success:
            return ApiResponse("created", message, data).response
        return ApiResponse("bad", message, data).response
    
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([MenuModelPermission])
def menuDetailView(request, pk):
    if request.method == "GET":
        success, message, data = getMenuDetailService(pk=pk)
        if success:
            return ApiResponse("ok", message, data).response
        return ApiResponse("bad", message,  data).response

    if request.method in ["PUT", "PATCH"]:
       success, message, data = updateMenuDetailService(pk=pk, requestData=request.data)
       if success:
            return ApiResponse("ok", message, data).response
       return ApiResponse("bad", message, data).response

    if request.method == "DELETE":
        success, message, data = deleteMenuService(pk=pk)
        if success:
            return ApiResponse("ok", message, data).response
        return ApiResponse("bad", message, data).response







