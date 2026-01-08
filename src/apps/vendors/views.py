# from src.services.vendors import * 
# from src.utils.apiResponse import ApiResponse
# from rest_framework.permissions import AllowAny
# from src.apps.vendors.permissions import VendorModelPermission
# from rest_framework.decorators import api_view, permission_classes
#
# @api_view(["GET", "POST"])
# @permission_classes([VendorModelPermission])
# def vendorsView(request):
#     if request.method == "GET":
#         success, message, data = vendorsListService() 
#         if success:
#             return ApiResponse("ok", message, data).response
#         return ApiResponse("bad", message, data).response
#
#     if request.method == "POST":
#         print("request.data", request.data)
#         success, message, data = createVendorService(requestData=request.data)
#         if success:
#             return ApiResponse("created", message, data).response
#         return ApiResponse("bad", message, data).response
#
# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# @permission_classes([VendorModelPermission])
# def vendorDetailView(request, pk):
#     if request.method == "GET":
#         success, message, data = getVendorDetailService(pk=pk)
#         if success:
#             return ApiResponse("ok", message, data).response
#         return ApiResponse("bad", message,  data).response
#
#     if request.method in ["PUT", "PATCH"]:
#        success, message, data = updateVendorDetailService(pk=pk, requestData=request.data)
#        if success:
#             return ApiResponse("ok", message, data).response
#        return ApiResponse("bad", message, data).response
#
#     if request.method == "DELETE":
#         success, message, data = deleteVendorService(pk=pk)
#         if success:
#             return ApiResponse("ok", message, data).response
#         return ApiResponse("bad", message, data).response
#


