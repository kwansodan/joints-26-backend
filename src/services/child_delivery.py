
from src.apps.bikers.models import Delivery
from src.apps.bikers.serializers import DeliverySerializer, VehicleSerializer


def deliveryListService():
    try:
        objs = Delivery.objects.all()
        serializer = DeliverySerializer(instance=objs, many=True)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[DeliveryService Err] Failed to get delivery list: {e}")
        return False, "failed", None


def createDeliveryService(requestData):
    try:
        delivery_serializer = DeliverySerializer(data=requestData)
        delivery_serializer.is_valid(raise_exception=True)
        delivery_serializer.save()
        return True, "success", None
    except Exception as e:
        print(f"[DeliveryService Err] Failed to create delivery: {e}")
        return False, "failed", None


def getDeliveryDetailService(pk):
    try:
        obj = Delivery.objects.get(pk=pk)
        serializer = DeliverySerializer(instance=obj)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[DeliveryService Err] Failed to get delivery detail: {e}")
        return False, "failed", None


def updateDeliveryDetailService(pk, requestData):
    try:
        delivery_instance = Delivery.objects.get(id=pk)
        delivery_serializer = DeliverySerializer(
            instance=delivery_instance, data=requestData
        )
        delivery_serializer.is_valid(raise_exception=True)
        delivery_serializer.save()
        return True, "success", None
    except Exception as e:
        print(f"[DeliveryService Err] Failed to update biker: {e}")
        return False, "failed", None


def deleteDeliveryDetailService(pk):
    try:
        obj = Delivery.objects.get(pk=pk)
        obj.delete()
        return True, "success", None
    except Exception as e:
        print(f"[DeliveryService Err] Failed to delete biker: {e}")
        return False, "failed", None
