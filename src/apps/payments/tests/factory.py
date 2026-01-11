from decimal import Decimal
from src.apps.orders.models import Order
from src.apps.payments.models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()

def create_payment(
    order: Order,
    paymentMethod="momo",
    paymentReference="ref-2343",
    ):
    payment = Payment.objects.create(
        order=order,
        paymentMethod=paymentMethod,
        paymentReference=paymentReference,
    )
    return payment 


