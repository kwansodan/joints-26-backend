from src.apps.vendors.models import Vendor
from src.apps.vendors.serializers import VendorSerializer

# users
def vendorsListService():
    status = False
    message = "Error fetching vendors" 
    data = None
    try:
        objs = Vendor.objects.all()
        serializer = VendorSerializer(instance=objs, many=True)
        if serializer:
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[VendorService Err] Failed to get vendors list: {e}")
    return status, message, data
    
def createVendorService(requestData):
    status = False
    message = "Failed to create vendor" 
    data = None
    try:
        serializer = VendorSerializer(data=requestData)
        if serializer.is_valid():
            serializer.save()
            status = True
            message = "Vendor created successfully"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[VendorService Err] Failed to create vendor: {e}")
    return status, message, data

def getVendorDetailService(pk):
    status = False
    message = "no vendor found"
    data = None
    try:
       obj = Vendor.objects.get(pk=pk)
       if obj:
            serializer = VendorSerializer(instance=obj)
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[VendorService Err] Failed to get vendor detail: {e}")
    return status, message, data

def updateVendorDetailService(pk, requestData):
    status = False
    message = "vendor does not exists" 
    data = None
    try:
        obj = Vendor.objects.get(pk=pk)
        if obj:
            serializer = VendorSerializer(instance=obj, data=requestData, partial=True)
            if serializer.is_valid():
                serializer.save()
                status = True
                message = "success"
                data = serializer.data
            else:
                status = False
                message = serializer.errors
    except Exception as e:
        print(f"[VendorService Err] Failed to update vendor: {e}")
    return status, message, data

def deleteVendorService(pk):
    status = False
    message = "vendor doest not exists" 
    data = None
    try:
        obj = Vendor.objects.get(pk=pk)
        if obj:
            obj.delete()
            status = True
            message = "success"
    except Exception as e:
        print(f"[VendorService Err] Failed to delete vendor: {e}")
    return status, message, data
