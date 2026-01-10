from src.apps.orders.models import Location
from src.apps.orders.serializers import LocationSerializer

# biker 
def locationListService():
    status = False
    message = "Error fetching locations" 
    data = None
    try:
        objs = Location.objects.all()
        serializer = LocationSerializer(instance=objs, many=True)
        if serializer:
            status = True
            message = "success"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[LocationService Err] Failed to get location list: {e}")
    return status, message, data
    
def createLocationService(requestData):
    status = False
    message = None
    data = None
    try:
        data = requestData.copy()
        serializer = LocationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            status = True
            message = "Location created successfully"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[LocationService Err] Failed to create location: {e}")
    return status, message, data

def getLocationDetailService(pk):
    status = False
    message = "no location found"
    data = None
    try:
       obj = Location.objects.get(pk=pk)
       if obj:
            serializer = LocationSerializer(instance=obj)
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[LocationService Err] Failed to get location detail: {e}")
    return status, message, data

def updateLocationDetailService(pk, requestData):
    status = False
    message = "location does not exists" 
    data = None
    try:
        obj = Location.objects.get(pk=pk)
        if obj:
            serializer = LocationSerializer(instance=obj, data=requestData, partial=True)
            if serializer.is_valid():
                serializer.save()
                status = True
                message = "success"
                data = serializer.data
            else:
                status = False
                message = serializer.errors
    except Exception as e:
        print(f"[LocationService Err] Failed to update location: {e}")
    return status, message, data

def deleteLocationService(pk):
    status = False
    message = "biker doest not exists" 
    data = None
    try:
        obj = Location.objects.get(pk=pk)
        if obj:
            obj.delete()
            status = True
            message = "success"
    except Exception as e:
        print(f"[LocationService Err] Failed to delete location: {e}")
    return status, message, data

