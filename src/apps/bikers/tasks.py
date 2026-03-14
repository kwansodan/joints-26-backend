from celery import Task, shared_task
from django.conf import settings
from django.db import transaction

from src.apps.bikers.models import ChildDeliveryItem, ParentDeliveryItem
from src.apps.orders.models import Order, OrderLocation
from src.services.server_sent_events import notify_frontend
from src.utils.sms_mnotify import Mnotifiy
from src.utils.wegoo import WeGoo

FRONTEND_URL = settings.FRONTEND_URL


class BaseTaskWithRetry(Task):
    max_retries = 5
    default_retry_delay = 60


@shared_task(bind=True, base=BaseTaskWithRetry)
@transaction.atomic
def dispatch_order_delivery_wegoo(
    self,
    order_id=None,
    parent_delivery_id=None,
    child_delivery_id=None,
    is_fulfilment_delivery=False,
    service=None,
    metadata=None,
    details=None,
):
    if not order_id:
        return {"status": False, "detail": "Can't dispatch order. No order id found"}

    if not parent_delivery_id:
        return {
            "status": False,
            "detail": "No parent delivery id. Can'tdispatch order without parent delivery id",
        }

    if not child_delivery_id:
        return {
            "status": False,
            "detail": "No sub delivery item id. Can't dispatch order without sub delivery item id",
        }

    if not details:
        return {"status": False, "detail": "No details provided"}

    if not metadata:
        return {"status": False, "detail": "No metadata provided"}

    if not service:
        return {"status": False, "detail": "No service type provided"}

    try:
        wegoo = WeGoo(
            is_fulfillment_delivery=is_fulfilment_delivery,
            service=service,
            details=details,
            recipient=metadata["recipient"],
            sender=metadata["sender"],
        )

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return {"status": False, "detail": "Order does not exist"}

        try:
            parentDelivery = ParentDeliveryItem.objects.get(id=parent_delivery_id)
        except ParentDeliveryItem.DoesNotExist:
            return {"status": False, "detail": "Parent delivery item does not exist"}

        try:
            childDelivery = ChildDeliveryItem.objects.get(id=child_delivery_id)
        except ChildDeliveryItem.DoesNotExist:
            return {"status": False, "detail": "Child delivery item not found"}

        if not order.paymentConfirmed or not order.customerLocationCaptured:
            return {
                "status": False,
                "detail": "order payment or customer location capture not completed",
            }

        delivery_status, tracking_number, delivery_type = wegoo.create_delivery()
        if not delivery_status:
            print("DELIVERY CREATION FAILED")
            return {"status": False, "detail": "failed to create delivery price"}

        # main boss
        updated = ChildDeliveryItem.objects.filter(id=child_delivery_id).update(
            dispatchAssigned=True,
            dispatchServiceTrackingNumber=tracking_number,
            dispatchServiceDeliveryType=delivery_type,
        )
        if updated > 0:
            vendor_name = metadata["sender"]["name"]
            vendor_phone = metadata["sender"]["phone"]
            dispatchService = "WeGoo"
            deliveryToken = childDelivery.deliveryTokenId
            order_package = ""

            for ditem in details["items"]:
                order_package += f" {ditem['quantity']} order(s) of {ditem['name']} "

            message = f"Hello {vendor_name}. A customter just placed {order_package}. A rider from {dispatchService} will be there in an hour to collect the package. Delivery token is {deliveryToken}."

            print("ALERTING VENDOR ON ORDER DELIVERY CREATED")
            print("sending message-----------------")
            print("TO---", vendor_name, "@", vendor_phone)
            print("MSG", message)
            print("message sent-----------------")

            # mnotify = Mnotifiy(recipients=[payload["phone"]], message=payload["message"])
            # _ = mnotify.send()

            ChildDeliveryItem.objects.filter(id=child_delivery_id).update(
                vendorNotified=True,
            )

            customer = order.customer
            if customer is not None:
                customer_fullname = customer.customer_fullname
                notify_frontend(
                    update_type="Order",
                    update_action="dispatch",
                    update_id=f"Order for {customer_fullname} successfully dispatched and vendor notified",
                    status=True,
                )
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
