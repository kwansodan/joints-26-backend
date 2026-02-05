from django.db import models
from src.utils.dbOptions import *
from src.apps.users.models import User
from src.utils.helpers import random_token

class Biker(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    status = models.BooleanField(default=False, null=True, blank=True)
    totalTrips = models.IntegerField(default=0, null=True, blank=True)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    @property
    def vehicles(self):
        from src.apps.bikers.serializers import VehicleSerializer
        vehicles = Vehicle.objects.filter(biker=self)
        return VehicleSerializer(instance=vehicles).data if len(vehicles) > 0 else []
 
    @property
    def userInfo(self):
        from src.apps.users.serializers import AuthSerializer
        user = User.objects.get(pk=self.user.pk)
        return AuthSerializer(instance=user).data if user else None 

    class _Meta:
        verbose_name_plural = "Biker"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.user} - {self.status}"

class Vehicle(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    biker = models.ForeignKey(Biker, on_delete=models.CASCADE, null=False, blank=False)
    vehicleType = models.CharField(max_length=TINY_STR_LEN, null=True, choices=VEHICLE_TYPE, default="bike", blank=True)
    licensePlate = models.CharField(max_length=TINY_STR_LEN, null=True, blank=True)
    registered = models.BooleanField(default=False, null=True, blank=True)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    @property
    def bikerId(self):
        return self.biker.pk if self.biker else ""

    class _Meta:
        verbose_name_plural = "Vehicle"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.biker.user.email} - {self.vehicleType} - {self.licensePlate}"
