from secrets import token_urlsafe

from celery import Task, shared_task
from django.conf import settings

from src.apps.external.models import GeneratedLink
from src.apps.orders.models import OrderLocation, Order
from src.utils.dbOptions import TOKEN_LEN
from src.utils.sms_mnotify import Mnotifiy

FRONTEND_URL = settings.FRONTEND_URL


class BaseTaskWithRetry(Task):
    max_retries = 5
    default_retry_delay = 60


@shared_task(bind=True, base=BaseTaskWithRetry)
def send_order_location_capture_link(self, location_id: str):
    try:
        location = OrderLocation.objects.get(pk=location_id)
        order = Order.objects.get(id=location.order.id)
        order.update_order_subtotal
    except OrderLocation.DoesNotExist as e:
        raise self.retry(exc=e, countdown=60)

    if location.captured:
        return {"status": "location already captured", "location_id": location_id}

    url_token = token_urlsafe(TOKEN_LEN)
    link = f"{FRONTEND_URL}locationcapture/order/{url_token}/{location.id}"
    generated_link = GeneratedLink.objects.create(
        category="order", token=url_token, link=link
    )

    recipients = [order.customer.phone]
    message = f"Hello {order.customer.first_name}. Thanks for placing an order with us. Please use the link below to share your location for delivery. {generated_link.link}"
    print("mesage", message)

    # try:
    #     mnotify = Mnotifiy(recipients=recipients, message=message)
    #     _ = mnotify.send()
    # except Exception as exc:
    #     raise self.retry(exc=exc)

    return {"status": "location capture link sent", "location_id": location_id}
