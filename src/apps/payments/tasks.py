from celery import Task, shared_task

from src.apps.orders.models import Order
from src.apps.payments.models import Payment, PaystackTransactionReference
from src.utils.sms_mnotify import Mnotifiy


class BaseTaskWithRetry(Task):
    max_retries = 5
    default_retry_delay = 60


@shared_task(bind=True, base=BaseTaskWithRetry)
def send_order_payment_link(self, order_id: str, paymentReference: str, auth_url: str):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist as e:
        raise self.retry(exc=e, countdown=60)

    if order.paymentConfirmed:
        return {"status": False, "detail": "payment already confirmed"}

    PaystackTransactionReference.objects.get_or_create(
        order=order, reference=paymentReference
    )
    recipients = [order.customer.phone]
    first_name = order.customer.first_name
    message = f"Hello {first_name}. Please make payment for your order using the link below. {auth_url}"
    print("message", message)

    # try:
    #     mnotify = Mnotifiy(recipients=recipients, message=message)
    #     _ = mnotify.send()
    # except Exception as exc:
    #     raise self.retry(exc=exc)

    return {"status": "order payment link sent", "order_id": order_id}
