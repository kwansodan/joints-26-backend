from src.utils.apiResponse import ApiResponse
from rest_framework.permissions import AllowAny
from src.apps.users.serializer import AuthSerializer
from src.apps.users.permissions import UserModelPermission
from rest_framework.decorators import api_view, permission_classes
from src.services.users import getUserDetailService, usersListService, addUserService, deleteUserService, updateUserService

@api_view(["GET", "POST"])
@permission_classes([UserModelPermission])
def usersView(request):
    if request.method == "GET":
        success, message, data = usersListService() 
        if success:
            return ApiResponse("ok", message, data).response
        return ApiResponse("bad", message, data).response

    if request.method == "POST":
        success, message, data = addUserService(userData=request.data)
        if success:
            return ApiResponse("created", message, data).response
        return ApiResponse("bad", message, data).response
    
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([UserModelPermission])
def userDetailView(request, pk):
    if request.method == "GET":
        success, message, data = getUserDetailService(userId=pk)
        if success:
            return ApiResponse("ok", message, data).response
        return ApiResponse("bad", message,  data).response

    if request.method in ["PUT", "PATCH"]:
       success, message, data = updateUserService(userId=pk, userData=request.data)
       if success:
            return ApiResponse("ok", message, data).response
       return ApiResponse("bad", message, data).response

    if request.method == "DELETE":
        success, message, data = deleteUserService(userId=pk)
        if success:
            return ApiResponse("ok", message, data).response
        return ApiResponse("bad", message, data).response















  
# def updatePasswordView(request):
#     user = request.user
#     if user:
#         oldPassword = request.data.get("oldPassword", "")
#         newPassword = request.data.get("newPassword", "")
#         if user.check_password(oldPassword):
#             user.set_password(newPassword)
#             user.save()
#         return ApiResponse("ok", "success", None).response
#     else:
#         return ApiResponse("bad", "failed", None).response
