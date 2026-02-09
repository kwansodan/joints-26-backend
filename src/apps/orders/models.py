from decimal import Decimal
from django.db import models
from src.utils.dbOptions import *
from src.apps.users.models import User
from src.apps.vendors.models import MenuItem
from src.utils.helpers import random_token

class Order(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    customer = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    subtotal = models.IntegerField(default=1, null=False, blank=False)
    specialNotes = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "Orders"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"Order - {self.customer}"

class Location(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=False, blank=False)
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
    processed = models.BooleanField(default=False)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "Location"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.displayName} - ({self.latitude}, {self.longitude})"

class OrderItem(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=False, blank=False)
    menuItem = models.OneToOneField(MenuItem, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(default=1, null=False, blank=False)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    # @property
    # def getMenuItems(self):
    #     from src.apps.vendors.serializers import MenuItemSerializer
    #     return MenuItemSerializer(instance=self.menuItem).data

    # @property
    # def orderTotal(self):
    #     return self.menuItem.price * self.quantity

    class _Meta:
        verbose_name_plural = "OrderItem"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.menuItem.name} - {self.quantity}"


