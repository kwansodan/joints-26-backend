from celery import Task, shared_task
from django.conf import settings

from src.apps.bikers.models import Delivery
from src.apps.orders.models import Order, OrderLocation
from src.services.server_sent_events import notify_frontend
from src.utils.sms_mnotify import Mnotifiy
from src.utils.wegoo import WeGoo

FRONTEND_URL = settings.FRONTEND_URL


class BaseTaskWithRetry(Task):
    max_retries = 5
    default_retry_delay = 60


@shared_task(bind=True, base=BaseTaskWithRetry)
def dispatch_order_delivery_wegoo(
    self,
    orderId=None,
    is_fulfilment_delivery=False,
    service="intracity",
    metadata=None,
    details=None,
):
    if not orderId:
        return {"status": False, "detail": "Can't dispatch order. No order id found"}

    if not details:
        return {"status": False, "detail": "No details provided"}

    if not metadata:
        return {"status": False, "detail": "No metadata provided"}

    try:
        wegoo = WeGoo(
            is_fulfillment_delivery=False,
            service="intracity",
            details=details,
            recipient=metadata["recipient"],
            sender=metadata["sender"],
        )

        try:
            order = Order.objects.get(id=orderId)
            delivery = Delivery.objects.get(orderId=order.id)
        except Order.DoesNotExist:
            return {"status": False, "detail": "Order not found"}

        if not order.paymentConfirmed or not order.customerLocationCaptured:
            return {
                "status": False,
                "detail": "order payment or customer location capture not completed",
            }

        delivery_status, tracking_number, delivery_type = wegoo.create_delivery()
        if not delivery_status:
            print("DELIVERY CREATION FAILED")
            return {"status": False, "detail": "failed to create delivery price"}

        # Delivery.objects.filter(
        #     orderId=orderId,
        # ).update(
        #     dispatchServiceTrackingNumber=tracking_number,
        #     dispatchServiceDeliveryType=delivery_type,
        # )
    except Exception as e:
        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, base=BaseTaskWithRetry)
def alert_vendor_on_order_delivery_created(self, deliveryId: str):
    message_payload = []

    try:
        delivery = Delivery.objects.get(pk=deliveryId)
        order = Order.objects.get(id=delivery.orderId)
    except OrderLocation.DoesNotExist as e:
        raise self.retry(exc=e, countdown=60)

    if not order.paymentConfirmed or not order.customerLocationCaptured:
        return {
            "status": False,
            "detail": "order payment or customer location capture not completed",
        }

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

        vendor_name = vendor.name
        item_quantity = item.quantity
        item_name = menuItem.name
        deliveryToken = delivery.deliveryTokenId
        dispatchService = delivery.dispatchService.capitalize()

        message = f"Hello {vendor_name}. A customter just placed {item_quantity} order(s) of {item_name}. A rider from {dispatchService} will be there in an hour to collect the package. Delivery token is {deliveryToken}."
        message_payload.append({"recipient": vendor.phone, "message": message})

    try:
        print("ALERTING VENDORS ON ORDER DELIVERY CREATED")
        for payload in message_payload:
            print("sending message-----------------")
            print("payload phone", payload["recipient"])
            print("payload message", payload["message"])
            print("message sent-----------------")

            # mnotify = Mnotifiy(recipients=[payload["phone"]], message=payload["message"])
            # _ = mnotify.send()

            updated = Delivery.objects.filter(id=deliveryId, orderId=order.id).update(
                vendorNotified=True
            )
            if updated > 0:
                Order.objects.filter(id=order.id).update(riderDispatched=True)
                # Delivery.

                customer = order.customer
                if customer is not None:
                    customer_fullname = customer.customer_fullname
                    notify_frontend(
                        update_type="Order",
                        update_action="dispatch",
                        update_id=f"Order for {customer_fullname} successfully dispatched and vendor notified",
                        status=True,
                    )
            else:
                print("delivery object not updated")

                # optionally send message to customer

    except Exception as exc:
        raise self.retry(exc=exc)
