from decimal import Decimal

from django.db import models

from src.apps.users.models import User
from src.utils.dbOptions import *
from src.utils.helpers import random_token


class Vendor(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=MAX_STR_LEN, unique=True, null=False, blank=True)
    phone = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    createdBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    updatedBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    @property
    def location(self):
        try:
            return VendorLocation.objects.get(vendor=self)
        except Exception:
            return

    @property
    def menuList(self):
        from src.apps.vendors.serializers import MenuItemSerializer
        try:
            obj = MenuItem.objects.filter(vendor=self)
            return MenuItemSerializer(instance=obj, many=True).data
        except Exception as e:
            print(f"error getting menulist for vendor: {e}")
            return []

    class _Meta:
        verbose_name_plural = "Vendors"
        ordering = ["createdAt"]

    def __str__(self):
        return f"{self.name} - {self.phone}"


class MenuItem(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, null=False, blank=False
    )
    name = models.CharField(max_length=MAX_STR_LEN, null=False, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        decimal_places=DECIMAL_PLACES, max_digits=MAX_DIGIT_LEN, default=Decimal(10.00)
    )
    createdBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    updatedBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "MenuItems"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.name} - {self.price}"


class VendorLocation(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, null=False, blank=False
    )
    displayName = models.CharField(max_length=MAX_STR_LEN, null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=MAX_DIGIT_LEN, decimal_places=MIN_DIGIT_LEN, default=Decimal("0.00")
    )
    longitude = models.DecimalField(
        max_digits=MAX_DIGIT_LEN, decimal_places=MIN_DIGIT_LEN, default=Decimal("0.00")
    )
    city = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    state = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    houseNumber = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    road = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    town = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    suburb = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    district = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    country = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    captured = models.BooleanField(default=False)
    createdBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    updatedBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "Vendor Location"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.vendor} - {self.city}"
