from src.apps.orders.models import Location
from src.apps.orders.serializers import LocationSerializer
from src.utils.workers import prep_wegoo_location_data, verify_location_capture_link


def locationListService():
    try:
        objs = Location.objects.all()
        serializer = LocationSerializer(instance=objs, many=True)
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
        serializer = LocationSerializer(instance=obj)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[LocationService Err] Failed to get location detail: {e}")
        return False, "failed", None


def updateLocationDetailService(pk, link_token, requestData):
    try:
        status = verify_location_capture_link(token=link_token, category="vendor")
        if not status:
            return False, "Invalid token", None

        data = requestData["data"]
        obj = Location.objects.get(pk=pk)
        if obj:
            serializer = LocationSerializer(instance=obj, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                location = serializer.save()
                print("location saved/updated")

                wegoo_status, wegoo_data = prep_wegoo_location_data(getattr(location, "id"))
                print("wegoo status", wegoo_status)
                print("wegoo data", wegoo_data)

                # prep wegoo destination and origin payload 
                # prep ordersitems for wegoo
                # create order delivery price wegoo
                # create delivery

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
