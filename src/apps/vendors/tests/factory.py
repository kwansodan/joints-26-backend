from src.apps.vendors.models import Vendor
from django.contrib.auth import get_user_model

User = get_user_model()

def create_vendor(user: User, name="test vendor", location="test location", phone="+2351412334"):
    vendor = Vendor.objects.create(
        user=user,
        name=name,
        location=location, 
        phone=phone
    )
    return vendor 
