from src.apps.orders.models import Order
from src.apps.vendors.models import Vendor, VendorLocation
from src.apps.vendors.serializers import VendorLocationSerializer
from src.utils.wegoo import WeGoo
from src.utils.workers import prep_wegoo_location_data, verify_location_capture_link


def updateOrderRiderDispatch(pk, requestData):
    try:
        order = Order.objects.get(id=pk)

        if not order.customerLocationCaptured:
            return False, "customer location not captured", None

        if order.riderDispatched:
            return True, "success", None

        status, wegoo_data = prep_wegoo_location_data(order_id=pk)
        if not status:
            return False, "Failed to prep wegoo data", None

        # get delivery price
        if wegoo_data is not None:
            for item in wegoo_data:
                wegoo = WeGoo(
                    is_fulfillment_delivery=False, service="intracity", details=item
                )
                status = wegoo.get_delivery_price()
                if status:
                    print("wegoo delivery item successfully created")

        return True, "success", None
        # obj = VendorLocation.objects.get(pk=pk)
        # serializer = VendorLocationSerializer(instance=obj, data=data, partial=True)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        # return True, "success", serializer.data
    except Exception as e:
        print(f"[WegooOrderDispatchService Err] Failed to dispatch wegoo order: {e}")
        return False, "failed", None
