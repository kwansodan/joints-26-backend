from src.apps.bikers.models import Biker, BikerVehicle
from src.apps.bikers.serializers import BikerSerializer, BikerVehicleSerializer

# biker 
def bikersListService():
    status = False
    message = "Error fetching bikers" 
    data = None
    try:
        objs = Biker.objects.all()
        serializer = BikerSerializer(instance=objs, many=True)
        if serializer:
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[BikerService Err] Failed to get bikers list: {e}")
    return status, message, data
    
def createBikerService(requestData):
    status = False
    message = None
    data = None
    try:
        data = requestData.copy()
        serializer = BikerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            status = True
            message = "Biker created successfully"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[BikerService Err] Failed to create biker: {e}")
    return status, message, data

def getBikerDetailService(pk):
    status = False
    message = "no biker found"
    data = None
    try:
       obj = Biker.objects.get(pk=pk)
       if obj:
            serializer = BikerSerializer(instance=obj)
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[BikerService Err] Failed to get biker detail: {e}")
    return status, message, data

def updateBikerDetailService(pk, requestData):
    status = False
    message = "biker does not exists" 
    data = None
    try:
        obj = Biker.objects.get(pk=pk)
        if obj:
            serializer = BikerSerializer(instance=obj, data=requestData, partial=True)
            if serializer.is_valid():
                serializer.save()
                status = True
                message = "success"
                data = serializer.data
            else:
                status = False
                message = serializer.errors
    except Exception as e:
        print(f"[BikerService Err] Failed to update biker: {e}")
    return status, message, data

def deleteBikerService(pk):
    status = False
    message = "biker doest not exists" 
    data = None
    try:
        obj = Biker.objects.get(pk=pk)
        if obj:
            obj.delete()
            status = True
            message = "success"
    except Exception as e:
        print(f"[BikerService Err] Failed to delete biker: {e}")
    return status, message, data


# biker vehicle
def bikerVehiclesListService():
    status = False
    message = "Error fetching biker vehicles" 
    data = None
    try:
        objs = BikerVehicle.objects.all()
        serializer = BikerVehicleSerializer(instance=objs, many=True)
        if serializer:
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[BikerVehicleService Err] Failed to get bikers vehicles list: {e}")
    return status, message, data
    
def createBikerVehicleService(requestData):
    status = False
    message = None
    data = None
    try:
        data = requestData.copy()
        serializer = BikerVehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            status = True
            message = "Biker vehicle created successfully"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[BikerVehicleService Err] Failed to create biker vehicle: {e}")
    return status, message, data

def getBikerVehicleDetailService(pk):
    status = False
    message = "no biker vehicle found"
    data = None
    try:
       obj = BikerVehicle.objects.get(pk=pk)
       if obj:
            serializer = BikerVehicleSerializer(instance=obj)
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[BikerVehicleService Err] Failed to get biker vehicle detail: {e}")
    return status, message, data

def updateBikerVehicleDetailService(pk, requestData):
    status = False
    message = "biker vehicle does not exists" 
    data = None
    try:
        obj = BikerVehicle.objects.get(pk=pk)
        if obj:
            serializer = BikerVehicleSerializer(instance=obj, data=requestData, partial=True)
            if serializer.is_valid():
                serializer.save()
                status = True
                message = "success"
                data = serializer.data
            else:
                status = False
                message = serializer.errors
    except Exception as e:
        print(f"[BikerVehicleService Err] Failed to update biker vehicle: {e}")
    return status, message, data

def deleteBikerVehicleService(pk):
    status = False
    message = "biker vehicle doest not exists" 
    data = None
    try:
        obj = Biker.objects.get(pk=pk)
        if obj:
            obj.delete()
            status = True
            message = "success"
    except Exception as e:
        print(f"[BikerVehicleService Err] Failed to delete biker vehicle: {e}")
    return status, message, data
