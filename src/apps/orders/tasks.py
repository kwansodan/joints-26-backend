from celery import shared_task, Task
from src.utils.sms_mnotify import Mnotifiy
from src.apps.orders.models import Order, Location

class BaseTaskWithRetry(Task):
    max_retries = 5
    default_retry_delay = 60

@shared_task(bind=True, base=BaseTaskWithRetry)
def send_location_capture_link(self, location_id: str):
    print("passed order id", location_id)
    try:
        location = Location.objects.get(pk=location_id) 
        order = Order.objects.get(id=location.order.id)
    except Location.DoesNotExist as e:
        raise self.retry(exc=e, countdown=60)
    
    if location.processed:
        return {"status": "location already captured", "location_id": location_id}

    recipients = [order.customer.phone]
    print("recipient", recipients)
    message = f"Hello {order.customer.first_name}. Please share your location for your order using the link below. http://localhost:3000/locationcapture/{order.id}" 

    try:
        mnotify = Mnotifiy(recipients=recipients, message=message)
        out = mnotify.send()
        print("mnotify send out", out)
    except Exception as exc:
        raise self.retry(exc=exc)

    # updated = Order.objects.filter(pk=order.pk, location__processed=False).update(location__pro=True)
    # if updated == 0:
    #     return

    return {"status": "location capture link sent", "location_id": location_id}

