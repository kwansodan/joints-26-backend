from django.db import transaction
from src.apps.bikers.models import Biker, Vehicle 
from src.apps.bikers.serializers import BikerSerializer, VehicleSerializer
from src.apps.users.models import User
from src.apps.users.serializers import AuthSerializer
from src.services.vehicles import createVehicleService
from src.utils.helpers import clean_db_error_msgs 

# biker 
def bikersListService():
    try:
        objs = Biker.objects.all()
        serializer = BikerSerializer(instance=objs, many=True)
        if serializer:
            return True, "success", serializer.data
        else:
            return False, serializer.errors, None 
    except Exception as e:
        print(f"[BikerService Err] Failed to get bikers list: {e}")
        return False, clean_db_error_msgs(str(e)), None 
    
def createBikerService(requestData):
    try:
        print("request data", requestData)
        bikerInfo = requestData.get("bikerInfo", None)
        newvehicles = requestData.get("newVehiclesPayload", None)

        with transaction.atomic():
            if bikerInfo is not None:
                user_serializer = AuthSerializer(data={**bikerInfo, "password": "securebiker@123", "userType": "biker"})
                if user_serializer.is_valid(raise_exception=True):
                    user = user_serializer.save()

                    biker_serializer = BikerSerializer(data={"user": getattr(user, "pk")}) 
                    if biker_serializer.is_valid(raise_exception=True):
                        biker = biker_serializer.save()

                        if len(newvehicles) > 0:
                            [item.update({"biker": getattr(biker, "pk")}) for item in newvehicles]
                            print("new vehicle data", newvehicles)
                            vehicle_serializer = VehicleSerializer(data=newvehicles, many=True)
                            if vehicle_serializer.is_valid(raise_exception=True):
                                vehicle_serializer.save()
                return True, "success", None
    except Exception as e:
        print(f"[BikerService Err] Failed to create biker: {e}")
        return False, clean_db_error_msgs(str(e)), None

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

