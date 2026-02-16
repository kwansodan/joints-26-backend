import uuid

from celery import Task, shared_task

from src.apps.orders.models import Order
from src.apps.payments.models import Payment, PaystackTransactionReference
from src.utils.dbOptions import PAYSTACK_TRANSACTION_REF_LEN
from src.utils.paystack import Paystack
from src.utils.sms_mnotify import Mnotifiy


class BaseTaskWithRetry(Task):
    max_retries = 5
    default_retry_delay = 60


@shared_task(bind=True, base=BaseTaskWithRetry)
def send_order_payment_link(self, trxRef_id: str):
    try:
        trxObj = PaystackTransactionReference.objects.get(id=trxRef_id)
    except PaystackTransactionReference.DoesNotExist as e:
        raise self.retry(exc=e, countdown=60)

    if trxObj.processed:
        return {"status": "True", "detail": "order payment link has already been sent"}

    order = trxObj.order
    if order.paymentConfirmed:
        return {"status": False, "detail": "payment already confirmed"}

    paymentRefString = str(uuid.uuid4())[:PAYSTACK_TRANSACTION_REF_LEN]
    print("passed payment ref string", paymentRefString)

    paystack = Paystack(
        amount=float(order.subtotal),
        email=order.customer.email,
        reference=paymentRefString,
        metadata={"order_id": order.id},
    )

    auth_url_status, auth_url = paystack.get_transaction_url()
    if not auth_url_status:
        return {"status": False, "detail": "Failed to get auth_url from paystack"}

    updated = PaystackTransactionReference.objects.filter(order=order).update(
        paymentLink=auth_url, reference=paymentRefString
    )

    if updated > 0:
        recipients = [order.customer.phone]
        first_name = order.customer.first_name
        message = f"Hello {first_name}. Please make payment for your order using the link below. {auth_url}"
        print("message", message)

        # try:
        #     mnotify = Mnotifiy(recipients=recipients, message=message)
        #     _ = mnotify.send()
        # except Exception as exc:
        #     raise self.retry(exc=exc)

        PaystackTransactionReference.objects.filter(
            order=order, processed=False
        ).update(processed=True)

        return {"status": "order payment link sent", "trxRef_id": trxRef_id}

    else:
        return


@shared_task(bind=True, base=BaseTaskWithRetry)
def verify_and_update_order_payment(self, trxRef: str):
    try:
        trxObj = PaystackTransactionReference.objects.get(
            reference=trxRef, processed=True
        )
    except PaystackTransactionReference.DoesNotExist as e:
        print("trxRef obj not found")
        raise self.retry(exc=e, countdown=60)

    orderObj = trxObj.order
    if not orderObj:
        print("no order found")
        return {"status": False, "detail": "Order not found", "trxRef": trxRef}

    paymentObj = orderObj.payment
    if not paymentObj:
        print("no payment found")
        return {"status": False, "detail": "Payment not found", "trxRef": trxRef}

    if orderObj.paymentConfirmed:
        print("payment already confirmed")
        return {
            "status": False,
            "detail": "payment for order already confirmed",
            "trxRef": trxRef,
        }

    paystack = Paystack()
    verification_status = paystack.verify_payment(trxRef)
    print("verification status", verification_status)
    if not verification_status:
        print("failed to verify payment ref from paystack")
        return {
            "status": False,
            "detail": "Failed to verify payment reference from paystack",
        }

    updated = Payment.objects.filter(order=orderObj).update(
        paymentStatus=True, paymentReference=trxRef, processed=True
    )
    if updated > 0:
        print("worker successfully updated payment object")
        Order.objects.filter(id=orderObj.id, paymentConfirmed=False).update(
            paymentConfirmed=True
        )
        print("order finally updated for payment. final payment close off")

        # try:
        #     mnotify = Mnotifiy(recipients=recipients, message=message)
        #     _ = mnotify.send()
        # except Exception as exc:
        #     raise self.retry(exc=exc)
        return {"status": True, "detail":" order payment confirmed", "trxRef_id": trxRef, "order_id": orderObj.id}
    else:
        print("this worker didnt update any rows of orders so returning")
        return





