from src.apps.orders.models import Location
from src.apps.orders.serializers import LocationSerializer

def locationListService():
    try:
        objs = Location.objects.all()
        serializer = LocationSerializer(instance=objs, many=True)
        if serializer:
            return True, "success", serializer.data
    except Exception as e:
        print(f"[LocationService Err] Failed to get location list: {e}")
        return False, "failed", None


def createLocationService(requestData):
    try:
        serializer = LocationSerializer(data=requestData)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return True, "success", serializer.data
    except Exception as e:
        print(f"[LocationService Err] Failed to create location: {e}")
        return False, "failed", None


def getLocationDetailService(pk):
    try:
        obj = Location.objects.get(pk=pk)
        if obj:
            serializer = LocationSerializer(instance=obj)
            return True, "success", serializer.data
    except Exception as e:
        print(f"[LocationService Err] Failed to get location detail: {e}")
        return False, "failed", None


def updateLocationDetailService(pk, requestData):
    try:
        obj = Location.objects.get(pk=pk)
        if obj:
            serializer = LocationSerializer(
                instance=obj, data=requestData, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                location = serializer.save()

                # create order delivery price

        return True, "success", serializer.data
    except Exception as e:
        print(f"[LocationService Err] Failed to update location: {e}")
        return False, "failed", None

def deleteLocationService(pk):
    try:
        obj = Location.objects.get(pk=pk)
        if obj:
            obj.delete()
        return True, "success", None
    except Exception as e:
        print(f"[LocationService Err] Failed to delete location: {e}")
        return False, "failed", None
