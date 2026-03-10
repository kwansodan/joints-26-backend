from celery import Task, shared_task
from django.conf import settings

from src.apps.bikers.models import Delivery
from src.apps.orders.models import Order, OrderLocation
from src.utils.sms_mnotify import Mnotifiy

FRONTEND_URL = settings.FRONTEND_URL


class BaseTaskWithRetry(Task):
    max_retries = 5
    default_retry_delay = 60


@shared_task(bind=True, base=BaseTaskWithRetry)
def alert_vendor_on_order_delivery_created(self, deliveryId: str):
    message_payload = {}

    try:
        delivery = Delivery.objects.get(pk=deliveryId)
        order = Order.objects.get(id=deliveryId.orderId)
    except OrderLocation.DoesNotExist as e:
        raise self.retry(exc=e, countdown=60)

    if not order.paymentConfirmed or not order.customerLocationCaptured:
        return {"status": False, "detail": "order payment or customer location capture not completed"}

    orderitems = order.orderitem_set.all()
    for item in orderitems:
        menuItem = item.menuItem
        vendor = item.menuItem.vendor

        if vendor is None:
            return {"status": "failed", "detail": "No vendor found"}

        if not vendor.phone:
            return {
                "status": "failed",
                "detail": "Vendor has no phone. Can't send message",
            }

        message = f"Hello {vendor.name}. A customter just placed {menuItem.quantity} orders for {menuItem.name}. A rider from {delivery.dispatchService} will be there in an hour to collect the package. Delivery token is {delivery.deliveryTokenId}."
        message_payload.update({"recipient": vendor.phone, "message": message})

    try:
        print("ALERTING VENDORS ON ORDER DELIVERY CREATED")
        for payload in message_payload:
            print("payload phone", payload["phone"])
            print("payload phone", payload["phone"])

            # mnotify = Mnotifiy(recipients=[payload["phone"]], message=payload["message"])
            # _ = mnotify.send()
    except Exception as exc:
        raise self.retry(exc=exc)

    return {
        "status": "success",
        "location_id": "vendor alert message successfully sent",
    }
