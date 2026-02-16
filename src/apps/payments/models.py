from django.db import models

from src.apps.orders.models import Order
from src.utils.dbOptions import *
from src.utils.helpers import random_token


class Payment(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=False, blank=False
    )
    paymentStatus = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    paymentMethod = models.CharField(
        max_length=MIN_STR_LEN,
        default="momo",
        choices=PAYMENT_OPTIONS,
        null=False,
        blank=False,
    )
    paymentReference = models.CharField(max_length=MIN_STR_LEN, null=False, blank=False)
    confirmedBy = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    createdBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    updatedBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "Order Payment"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"Order payment {self.order.id} - {self.processed}"


class PaystackTransactionReference(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=False, blank=False, related_name="paystackTrxRefObj"
    )
    paymentLink = models.CharField(max_length=MAX_STR_LEN, null=False, blank=True)
    reference = models.CharField(max_length=MIN_STR_LEN, null=False, blank=True)
    processed = models.BooleanField(default=False)
    createdBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    updatedBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "Paystack Transaction Ref"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"Trans Ref {self.order.id} - {self.reference}"

