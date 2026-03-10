from django.db import transaction

from src.apps.vendors.models import VendorRedeemToken
from src.apps.vendors.serializers import VendorRedeemTokenSerializer


def vendorRedeemTokenListService():
    try:
        objs = VendorRedeemToken.objects.all()
        serializer = VendorRedeemTokenSerializer(instance=objs, many=True)
        if serializer:
            return True, "success", serializer.data
        else:
            return False, serializer.errors, None
    except Exception as e:
        print(f"[VendorRedeemTokenService Err] Failed to get vendor redeem token  list: {e}")
        return False, "failed", None


def createVendorRedeemTokenService(requestData):
    try:
        vendorredeemToken_serializer = VendorRedeemTokenSerializer(data=requestData)
        vendorredeemToken_serializer.is_valid(raise_exception=True)
        vendorredeemToken_serializer.save()
        return True, "success", None
    except Exception as e:
        print(f"[VendorRedeemTokenService Err] Failed to vendor redeem token : {e}")
        return False, "failed", None


def getVendorRedeemTokenDetailService(pk):
    try:
        obj = VendorRedeemToken.objects.get(pk=pk)
        serializer = VendorRedeemTokenSerializer(instance=obj)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[VendorRedeemTokenService Err] Failed to get vendor redeem token detail: {e}")
        return False, "failed", None


def updateVendorRedeemTokenDetailService(pk, requestData):
    try:

        instance = VendorRedeemToken.objects.get(id=pk)
        vendorredeemToken_serializer = VendorRedeemTokenSerializer(
            instance=instance, data=requestData
        )
        vendorredeemToken_serializer.is_valid(raise_exception=True)
        vendorredeemToken_serializer.save()
        return True, "success", None
    except Exception as e:
        print(f"[VendorRedeemTokenService Err] Failed to update vendor redeem token : {e}")
        return False, "failed", None


def deleteVendorRedeemTokenService(pk):
    try:
        obj = VendorRedeemToken.objects.get(pk=pk)
        obj.delete()
        return True, "success", None
    except Exception as e:
        print(f"[VendorRedeemTokenService Err] Failed to delete vendor redeem token : {e}")
        return False, "failed", None
