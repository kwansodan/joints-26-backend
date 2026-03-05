from django.db import transaction

from src.apps.bikers.models import Biker, Vehicle
from src.apps.bikers.serializers import BikerSerializer, VehicleSerializer
from src.apps.users.models import User
from src.apps.users.serializers import AuthSerializer
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
                            vehicle_serializer = VehicleSerializer(data=newvehicles, many=True)
                            if vehicle_serializer.is_valid(raise_exception=True):
                                vehicle_serializer.save()
            return True, "success", None
    except Exception as e:
        print(f"[BikerService Err] Failed to create biker: {e}")
        return False, clean_db_error_msgs(str(e)), None

def getBikerDetailService(pk):
    try:
        obj = Biker.objects.get(pk=pk)
        serializer = BikerSerializer(instance=obj)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[BikerService Err] Failed to get biker detail: {e}")
        return False, "failed", None

def updateBikerDetailService(pk, requestData):
    try:
        bikerId = requestData.get("bikerId")
        bikerInfo = requestData.get("bikerUserInfo", None)
        newvehicles = requestData.get("newVehicles", None)
    
        with transaction.atomic():
            if bikerInfo is not None:

                userId = bikerInfo.get("id", None)
                user_instance = User.objects.get(pk=userId)

                biker_instance = Biker.objects.get(id=bikerId)
                biker_serializer = BikerSerializer(instance=biker_instance, data={"user": userId,"status": bikerInfo.get("status", False)})
                biker_serializer.is_valid(raise_exception=True)
                biker_serializer.save()

                user_serializer = AuthSerializer(instance=user_instance, data=bikerInfo, partial=True)
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()

            if newvehicles is not None and len(newvehicles) > 0:
                [item.update({"biker": pk}) for item in newvehicles]
                for item in newvehicles:
                    vehicle_instance = Vehicle.objects.get(pk=item["id"])
                    vehicle_serializer = VehicleSerializer(instance=vehicle_instance, data=item, partial=True)
                    if vehicle_serializer.is_valid(raise_exception=True):
                        vehicle_serializer.save()

            return True, "success", None
    except Exception as e:
        print(f"[BikerService Err] Failed to update biker: {e}")
        return False, clean_db_error_msgs(str(e)), None

def deleteBikerService(pk):
    try:
        obj = Biker.objects.get(pk=pk)
        if obj:
            obj.delete()
            return True, "success", None
    except Exception as e:
        print(f"[BikerService Err] Failed to delete biker: {e}")
        return False, clean_db_error_msgs(str(e)), None

