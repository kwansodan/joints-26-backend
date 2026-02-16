from src.apps.orders.models import OrderLocation
from src.apps.orders.serializers import OrderLocationSerializer, OrderSerializer
from src.utils.workers import (
    prep_wegoo_delivery_price_detail,
    verify_location_capture_link,
)


def orderLocationListService():
    try:
        objs = OrderLocation.objects.all()
        serializer = OrderLocationSerializer(instance=objs, many=True)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[OrderLocationService Err] Failed to get order location list: {e}")
        return False, "failed", None


def createOrderLocationService(requestData):
    try:
        serializer = OrderLocationSerializer(data=requestData)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return True, "success", serializer.data
    except Exception as e:
        print(f"[OrderLocationService Err] Failed to create order location: {e}")
        return False, "failed", None


def getOrderLocationDetailService(token, order_location_id):
    print("getting from order locaiton here")
    print("token", token)
    try:
        token_valid = verify_location_capture_link(token=token, category="order")
        if not token_valid:
            return False, "Invalid token", None

        orderLocationObj = OrderLocation.objects.get(pk=order_location_id)
        serializer = OrderSerializer(instance=orderLocationObj.order)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[OrderLocationService Err] Failed to get order location detail: {e}")
        return False, "Invalid token", None


def updateOrderLocationDetailService(token, order_location_id, requestData):
    try:
        token_valid = verify_location_capture_link(token=token, category="order")
        if not token_valid:
            return False, "Invalid token", None

        data = requestData["data"]
        obj = OrderLocation.objects.get(pk=order_location_id)
        if obj:
            serializer = OrderLocationSerializer(instance=obj, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                order_location = serializer.save()

                # wegoo_status, wegoo_data = prep_wegoo_delivery_price_detail(
                #     getattr(location, "id")
                # )

                # prep wegoo destination and origin payload
                # prep ordersitems for wegoo
                # create order delivery price wegoo
                # create delivery

        return True, "success", serializer.data
    except Exception as e:
        print(f"[OrderLocationService Err] Failed to update order location: {e}")
        return False, "failed", None


def deleteOrderLocationService(pk):
    try:
        obj = OrderLocation.objects.get(pk=pk)
        if obj:
            obj.delete()
        return True, "success", None
    except Exception as e:
        print(f"[OrderLocationService Err] Failed to delete order location: {e}")
        return False, "failed", None
