from django.db import transaction

from src.apps.orders.models import Order
from src.apps.payments.models import Payment, PaystackTransactionReference
from src.apps.payments.tasks import verify_and_update_order_payment
from src.utils.paystack import Paystack


def updateCustomerOrderPayment(pk, requestData):
    try:
        print("request data", requestData)
        requestAction = requestData.get("action")
        order = Order.objects.get(id=pk)
        if not order:
            return False, "Order not found", None

        if not order.customerLocationCaptured:
            return False, "Customer location must be captured before payment", None

        paymentObj, _ = Payment.objects.get_or_create(order=order)
        if order.paymentConfirmed and paymentObj.processed:
            return True, "Payment already confirmed", None

        if requestAction == "link":
            if order.subtotal < 1:
                order.update_order_subtotal

            paystackTrxRefExists, created = (
                PaystackTransactionReference.objects.get_or_create(order=order)
            )
            if not created:
                if paystackTrxRefExists.processed:
                    alltrxRefs = PaystackTransactionReference.objects.filter(
                        order=order
                    )
                    [trxRef.delete() for trxRef in alltrxRefs]
                    PaystackTransactionReference.objects.create(order=order)
            return True, "Success. Payment link has been sent to customer", None

        elif requestAction == "verify":
            with transaction.atomic():
                # final order payment page confirmation
                trxRef = requestData.get("trxRef")
                reference = requestData.get("reference")

                # shared task to update payment status
                verification_results = verify_and_update_order_payment.apply_async(
                    args=(trxRef), task_id=order.id, retry=False
                )

                if verification_results.ready():
                    print(
                        "results from order paymetn verification task",
                        verification_results.result,
                    )

                return True, "verifcation success", None

        else:
            return False, "Invalid action", None

    except Exception as e:
        print(
            f"[PaystackCustomerOrder Err] Failed to update customer order package payments: {e}"
        )
        return False, "failed", None
