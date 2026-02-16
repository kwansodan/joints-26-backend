from django.db import transaction

from src.apps.orders.models import Order
from src.apps.payments.models import Payment, PaystackTransactionReference
from src.apps.payments.tasks import (
    send_order_payment_link,
    verify_and_update_order_payment,
)
from src.utils.paystack import Paystack


def updateCustomerOrderPayment(pk, requestData):
    try:
        print("request data", requestData)
        requestAction = requestData.get("action")

        if requestAction == "link":
            order = Order.objects.get(id=pk)
            if not order:
                return False, "Order not found", None

            if not order.customerLocationCaptured:
                return False, "Customer location must be captured before payment", None

            paymentObj, _ = Payment.objects.get_or_create(order=order)
            if order.paymentConfirmed and paymentObj.processed:
                return True, "Payment already confirmed", None

            if order.subtotal < 1:
                order.update_order_subtotal

            paystackTrxRefExists, _ = (
                PaystackTransactionReference.objects.get_or_create(order=order)
            )

            trxRefId = paystackTrxRefExists.id
            res = send_order_payment_link.apply_async(
                args=(trxRefId,), task_id=trxRefId, retry=False
            )

            if res.ready():
                print("results from send payment link", res.result)
            return True, "Success. Payment link has been sent to customer", None

        elif requestAction == "verify":
            print("WORKING ON VERYFYING CUSTOMER ORDER PAYMENT")
            trxRef = requestData.get("trxref")

            trxRefObj = PaystackTransactionReference.objects.get(reference=trxRef)
            orderObj = trxRefObj.order

            if orderObj.paymentConfirmed:
                return True, "Payment already confirmed", {"order_id": orderObj.id}

            verify_and_update_order_payment.apply_async(
                args=(trxRef,), task_id=trxRef, retry=False
            )

            return True, "Verifying transaction...", {"order_id": orderObj.id}
        else:
            return False, "Invalid action", None

    except Exception as e:
        print(
            f"[PaystackCustomerOrder Err] Failed to update customer order package payments: {e}"
        )
        return False, "failed", None
