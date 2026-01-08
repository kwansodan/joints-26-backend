# from src.services.bikers import *
# from src.utils.apiResponse import ApiResponse
# from src.apps.bikers.permissions import BikerPermissionList
# from rest_framework.decorators import api_view, permission_classes
#
# # biker
# @api_view(["GET", "POST"])
# @permission_classes(BikerPermissionList)
# def bikerView(request):
#     if request.method == "GET":
#         success, message, data = bikersListService() 
#         if success:
#             return ApiResponse("ok", message, data).response
#         return ApiResponse("bad", message, data).response
#
#     if request.method == "POST":
#         success, message, data = createBikerService(requestData=request.data)
#         if success:
#             return ApiResponse("created", message, data).response
#         return ApiResponse("bad", message, data).response
#
# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# @permission_classes(BikerPermissionList)
# def bikerDetailView(request, pk):
#     if request.method == "GET":
#         success, message, data = getBikerDetailService(pk=pk)
#         if success:
#             return ApiResponse("ok", message, data).response
#         return ApiResponse("bad", message,  data).response
#
#     if request.method in ["PUT", "PATCH"]:
#        success, message, data = updateBikerDetailService(pk=pk, requestData=request.data)
#        if success:
#             return ApiResponse("ok", message, data).response
#        return ApiResponse("bad", message, data).response
#
#     if request.method == "DELETE":
#         success, message, data = deleteBikerService(pk=pk)
#         if success:
#             return ApiResponse("ok", message, data).response
#         return ApiResponse("bad", message, data).response
#
# # biker vehicle
# @api_view(["GET", "POST"])
# @permission_classes(BikerPermissionList)
# def bikerVehicleView(request):
#     if request.method == "GET":
#         success, message, data = bikerVehiclesListService() 
#         if success:
#             return ApiResponse("ok", message, data).response
#         return ApiResponse("bad", message, data).response
#
#     if request.method == "POST":
#         success, message, data = createBikerVehicleService(requestData=request.data)
#         if success:
#             return ApiResponse("created", message, data).response
#         return ApiResponse("bad", message, data).response
#
# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# @permission_classes(BikerPermissionList)
# def bikerVehicleDetailView(request, pk):
#     if request.method == "GET":
#         success, message, data = getBikerVehicleDetailService(pk=pk)
#         if success:
#             return ApiResponse("ok", message, data).response
#         return ApiResponse("bad", message,  data).response
#
#     if request.method in ["PUT", "PATCH"]:
#        success, message, data = updateBikerVehicleDetailService(pk=pk, requestData=request.data)
#        if success:
#             return ApiResponse("ok", message, data).response
#        return ApiResponse("bad", message, data).response
#
#     if request.method == "DELETE":
#         success, message, data = deleteBikerVehicleService(pk=pk)
#         if success:
#             return ApiResponse("ok", message, data).response
#         return ApiResponse("bad", message, data).response
#

