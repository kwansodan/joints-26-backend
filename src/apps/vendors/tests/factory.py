from src.apps.vendors.models import Vendor, MenuItem
from django.contrib.auth import get_user_model

User = get_user_model()

def create_vendor(
    user: User, 
    name="test vendor", 
    location="test location", 
    phone="+2351412334"
    ):
    vendor = Vendor.objects.create(
        user=user,
        name=name,
        location=location, 
        phone=phone
    )
    return vendor 

def create_menuitem(
        vendor: Vendor, 
        name="Fried Rice & Chicken", 
        description="Affordaable", 
        price=100.00
    ):
    menuitem = MenuItem.objects.create(
        vendor=vendor,
        name=name,
        description=description, 
        price=price
    )
    return menuitem
