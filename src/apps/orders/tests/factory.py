from decimal import Decimal
from django.contrib.auth import get_user_model
from src.apps.orders.models import Location, OrderItem, Order

User = get_user_model()

def create_location(
    displayName="Tabora",
    latitude=Decimal(0.5),
    longitude=Decimal(3.5),
    region="Greater Accra",
    district="Ga West",
    city="Accra",
    houseNumber="GW-1234-5678",
    road="Chantan",
    ):
    location = Location.objects.create(
        displayName=displayName,
        latitude=latitude, 
        longitude=longitude,
        region=region,
        district=district,
        city=city,
        houseNumber=houseNumber,
        road=road,
    )
    return location 

