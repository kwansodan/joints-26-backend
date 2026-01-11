from decimal import Decimal
from django.db import models
from src.utils.dbOptions import *
from src.apps.orders.models import Order
from src.utils.helpers import random_token

class Payment(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    paymentId = models.CharField(default=random_token, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=False, blank=False)
    status = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=MAX_DIGIT_LEN, decimal_places=DECIMAL_PLACES, default=Decimal(10.00))
    paymentMethod = models.CharField(max_length=MIN_STR_LEN, default="momo", choices=PAYMENT_OPTIONS, null=False, blank=False)
    paymentReference = models.CharField(max_length=MIN_STR_LEN, null=False, blank=False)
    confirmedBy = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "Payment"
        ordering = ["-createdAt"]

    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.order.orderSubtotal
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.paymentId} - {self.amount}, {self.status}"


