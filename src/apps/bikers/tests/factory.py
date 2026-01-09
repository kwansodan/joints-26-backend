from django.contrib.auth import get_user_model
from src.apps.bikers.models import Biker, Vehicle

User = get_user_model()

def create_biker(user: User):
    biker = Biker.objects.create(
        user=user,
        status=False,
        totalTrips=75
    )
    return biker 

def create_vehicle(biker: Biker, vehicleType="motorbike", licensePlate="GW-118-23", registered=True):
    vehicle = Vehicle.objects.create(
        biker=biker,
        vehicleType=vehicleType,
        licensePlate=licensePlate,
        registered=registered,
    )
    return vehicle
