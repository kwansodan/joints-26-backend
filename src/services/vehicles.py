from src.apps.bikers.models import Vehicle
from src.apps.bikers.serializers import VehicleSerializer 

def vehiclesListService():
    status = False
    message = "Error fetching vehicles" 
    data = None
    try:
        objs = Vehicle.objects.all()
        serializer = VehicleSerializer(instance=objs, many=True)
        if serializer:
            status = True
            message = "success"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[VehicleService Err] Failed to get vehicles list: {e}")
    return status, message, data
    
def createVehicleService(requestData):
    status = False
    message = None
    data = None
    try:
        data = requestData.copy()
        serializer = VehicleSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            status = True
            message = "Vehicle created successfully"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[VehicleService Err] Failed to create vehicle: {e}")
    return status, message, data

def getVehicleDetailService(pk):
    status = False
    message = "no vehicle found"
    data = None
    try:
       obj = Vehicle.objects.get(pk=pk)
       if obj:
            serializer = VehicleSerializer(instance=obj)
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[VehicleService Err] Failed to get vehicle detail: {e}")
    return status, message, data

def updateVehicleDetailService(pk, requestData):
    status = False
    message = "vehicle does not exists" 
    data = None
    try:
        obj = Vehicle.objects.get(pk=pk)
        if obj:
            serializer = VehicleSerializer(instance=obj, data=requestData, partial=True)
            if serializer.is_valid():
                serializer.save()
                status = True
                message = "success"
                data = serializer.data
            else:
                status = False
                message = serializer.errors
    except Exception as e:
        print(f"[VehicleService Err] Failed to update vehicle: {e}")
    return status, message, data

def deleteVehicleService(pk):
    status = False
    message = "vehicle doest not exists" 
    data = None
    try:
        obj = Vehicle.objects.get(pk=pk)
        if obj:
            obj.delete()
            status = True
            message = "success"
    except Exception as e:
        print(f"[VehicleService Err] Failed to delete vehicle: {e}")
    return status, message, data
