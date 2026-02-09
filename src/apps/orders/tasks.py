from celery import Task, shared_task
from django.conf import settings

from src.apps.orders.models import Location, Order
from src.utils.sms_mnotify import Mnotifiy

FRONTEND_URL = settings.FRONTEND_URL


class BaseTaskWithRetry(Task):
    max_retries = 5
    default_retry_delay = 60


@shared_task(bind=True, base=BaseTaskWithRetry)
def send_location_capture_link(self, location_id: str):
    try:
        location = Location.objects.get(pk=location_id)
        order = Order.objects.get(id=location.order.id)
    except Location.DoesNotExist as e:
        raise self.retry(exc=e, countdown=60)

    if location.processed:
        return {"status": "location already captured", "location_id": location_id}

    recipients = [order.customer.phone]
    link = f"{FRONTEND_URL}locationcapture/{order.id}"
    print("recipient", recipients)
    message = f"Hello {order.customer.first_name}. Thanks for placing an order with us. Please use the link below to share your location for delivery. {link}"
    print("mesage", message)

    # try:
    #     mnotify = Mnotifiy(recipients=recipients, message=message)
    #     _ = mnotify.send()
    # except Exception as exc:
    #     raise self.retry(exc=exc)

    return {"status": "location capture link sent", "location_id": location_id}
