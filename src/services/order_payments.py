from rest_framework.fields import uuid

from src.apps.orders.models import Order
from src.apps.payments.models import Payment, PaystackTransactionReference
from src.apps.payments.tasks import send_order_payment_link
from src.utils.dbOptions import PAYSTACK_TRANSACTION_REF_LEN
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
            print("JUST GETTING LINK")
            if order.subtotal < 1:
                order.update_order_subtotal
            paymentRefString = str(uuid.uuid4())[:PAYSTACK_TRANSACTION_REF_LEN]
            print("reference passed", paymentRefString)
            paystack = Paystack(
                amount=float(order.subtotal),
                email=order.customer.email,
                reference=paymentRefString,
                metadata={"order_id": order.id},
            )
            url_status, url_data = paystack.get_transaction_url()
            if not url_status:
                return False, "Failed to generate transaction url", None

            send_order_payment_link.apply_async(
                args=(order.pk, paymentRefString, url_data),
                task_id=order.id,
                retry=False,
            )
            return True, "Success. Transaction url sent to customer", url_data
        elif requestAction == "verify":
            print("JUST VERIFYING TRANSACTION")
            # final order payment page confirmation
            trxRef = requestData.get("trxRef")
            reference = requestData.get("reference")
            paystack = Paystack()
            transaction_valid = paystack.verify_payment(trxRef)
            if not transaction_valid:
                return False, "Transaction verification failed. Please try again", None
            return True, "Successfully verified transaction", None
        else:
            return False, "Invalid action", None
    except Exception as e:
        print(
            f"[PaystackCustomerOrder Err] Failed to update customer order package payments: {e}"
        )
        return False, "failed", None
