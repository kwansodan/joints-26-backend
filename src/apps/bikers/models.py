from django.db import models
from src.utils.dbOptions import *
from src.utils.helpers import random_token
from src.apps.users.models import User 

class Biker(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    status = models.BooleanField(default=False, null=True, blank=True)
    totalTrips = models.IntegerField(default=0, null=True, blank=True)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "Biker"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.user} - {self.status}"

class Vehicle(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    biker = models.ForeignKey(Biker, on_delete=models.CASCADE, null=False, blank=False)
    vehicleType = models.CharField(max_length=TINY_STR_LEN, null=True, choices=VEHICLE_TYPE, default="motorbike", blank=True)
    licensePlate = models.CharField(max_length=TINY_STR_LEN, null=True, blank=True)
    registered = models.BooleanField(default=False, null=True, blank=True)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "Vehicle"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.biker.user.name} - {self.vehicleType} - {self.licensePlate}"
