from celery import shared_task, Task
from src.utils.sms_mnotify import Mnotifiy
from src.apps.payments.models import Payment
from src.apps.orders.models import Order

class BaseTaskWithRetry(Task):
    max_retries = 5
    default_retry_delay = 60

@shared_task(bind=True, base=BaseTaskWithRetry)
def send_order_payment_link(self, payment_id: str):
    try:
        payment = Payment.objects.get(pk=payment_id) 
        order = Order.objects.get(id=payment.order.id)
    except Payment.DoesNotExist as e:
        raise self.retry(exc=e, countdown=60)
    
    if payment.processed:
        return {"status": "payment already processed", "location_id": payment_id}

    recipients = [order.customer.phone]
    link = f"https://api.paystack.com/pay/order-payment-{str(order.id)[:10]}"
    message = f"Hello {order.customer.first_name}. Please make payment for your order using the link below. {link}" 

    try:
        mnotify = Mnotifiy(recipients=recipients, message=message)
        _ = mnotify.send()
    except Exception as exc:
        raise self.retry(exc=exc)

    return {"status": "order payment link sent", "payment_id":payment_id}

