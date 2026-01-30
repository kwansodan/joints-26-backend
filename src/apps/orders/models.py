from decimal import Decimal
from django.db import models
from src.utils.dbOptions import *
from src.apps.users.models import User
from src.apps.vendors.models import MenuItem
from src.utils.helpers import random_token

class Location(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    displayName = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    latitude = models.DecimalField(max_digits=MAX_DIGIT_LEN, decimal_places=DECIMAL_PLACES, default=Decimal("0.00"))
    longitude = models.DecimalField(max_digits=MAX_DIGIT_LEN, decimal_places=DECIMAL_PLACES, default=Decimal("0.00"))
    region = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    district = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    city = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    town = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    suburb = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    houseNumber = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    road = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "Location"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.displayName} - ({self.latitude}, {self.longitude})"

class Order(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    subtotal = models.IntegerField(default=1, null=False, blank=False)
    status = models.BooleanField(default=False, null=True, blank=True)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    @property
    def getCustomer(self):
        from src.apps.users.serializers import AuthSerializer
        return AuthSerializer(instance=self.customer).data

    @property
    def orderItems(self):
        from src.apps.orders.serializers import OrderItemSerializer
        data = OrderItemSerializer(instance=OrderItem.objects.filter(order=self), many=True).data
        return data

    @property
    def orderSubtotal(self):
        prices = [item.menuItem.price * item.quantity for item in self.orderItems]
        print("prices", prices)
        return sum(prices)

    @property
    def orderActions(self):
        return {
            "has_location": False,
            "has_payment": False,
            "has_biker": False,
        }

    class _Meta:
        verbose_name_plural = "Orders"
        ordering = ["-createdAt"]

    def save(self, *args, **kwargs):
        if not self.subtotal:
            self.subtotal = self.orderSubtotal
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order to - {self.location}"

class OrderItem(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False)
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(default=1, null=False, blank=False)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    @property
    def getMenuItem(self):
        from src.apps.vendors.serializers import MenuItemSerializer
        return MenuItemSerializer(instance=self.menuItem).data

    @property
    def orderTotal(self):
        return self.menuItem.price * self.quantity

    class _Meta:
        verbose_name_plural = "OrderItem"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.menuItem.name} - {self.quantity}"


