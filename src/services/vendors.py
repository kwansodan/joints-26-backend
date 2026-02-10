import uuid

from django.db import transaction

from src.apps.users.models import User
from src.apps.users.serializers import AuthSerializer
from src.apps.vendors.models import Vendor
from src.apps.vendors.serializers import VendorLocationSerializer, VendorSerializer
from src.utils.workers import clean_email


# users
def vendorsListService():
    try:
        objs = Vendor.objects.all()
        serializer = VendorSerializer(instance=objs, many=True)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[VendorService Err] Failed to get vendors list: {e}")
        return False, "failed", None


def createVendorService(requestData):
    try:
        name = requestData.get("name", None)
        phone = requestData.get("phone", None)
        email = clean_email(f"{name}{str(uuid.uuid4())[:6]}@gmail.com")
    
        with transaction.atomic():
            user_serializer = AuthSerializer(
                data={
                    "first_name": f"fn _{name}",
                    "last_name": f"ln_{name}",
                    "email": email,
                    "phone": phone,
                    "password": f"securevendorr@{phone}",
                    "userType": "vendor",
                }
            )
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                user = user_serializer.data

                vendor_serializer = VendorSerializer(
                    data={"user": dict(user)["id"], "name": name, "phone": phone}
                )
                if vendor_serializer.is_valid(raise_exception=True):
                    vendor = vendor_serializer.save()

                    vendor_location_serializer = VendorLocationSerializer(
                        data={"vendor": getattr(vendor, "id")}
                    )
                    if vendor_location_serializer.is_valid(raise_exception=True):
                        vendor_location_serializer.save()
            return True, "success", vendor_serializer.data
    except Exception as e:
        print(f"[VendorService Err] Failed to create vendor: {e}")
        return False, "failed", None

def getVendorDetailService(pk):
    try:
        obj = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(instance=obj)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[VendorService Err] Failed to get vendor detail: {e}")
        return False, "failed", None

def updateVendorDetailService(pk, requestData):
    try:
        obj = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(instance=obj, data=requestData, partial=True)
        if serializer.is_valid():
            serializer.save()
        return True, "success", serializer.data
    except Exception as e:
        print(f"[VendorService Err] Failed to update vendor: {e}")
        return False, "failed", None

def deleteVendorService(pk):
    try:
        obj = Vendor.objects.get(pk=pk)
        obj.delete()
        return True, "success", None
    except Exception as e:
        print(f"[VendorService Err] Failed to delete vendor: {e}")
        return False, "failed", None
