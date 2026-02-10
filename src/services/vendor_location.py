from src.apps.vendors.models import Vendor, VendorLocation
from src.apps.vendors.serializers import VendorLocationSerializer
from src.utils.workers import prep_wegoo_location_data, verify_location_capture_link


# users
def vendorLocationListService():
    try:
        objs = VendorLocation.objects.all()
        serializer = VendorLocationSerializer(instance=objs, many=True)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[VendorLocationService Err] Failed to get vendors location list: {e}")
        return False, "failed", None


def createVendorLocationService(requestData):
    try:
        vendor_id = requestData.get("vendor_id", None)
        locationData = requestData.get("locationData", None)

        print("vendor_id", vendor_id)
        print("location data", locationData)
        print("vendor_id", vendor_id)

        vendor = Vendor.objects.get(id=vendor_id)
        if vendor:
            vendor_location_serializer = VendorLocationSerializer(
                data={
                    "vendor": vendor.id,
                }
            )
            if vendor_location_serializer.is_valid(raise_exception=True):
                vendor_location_serializer.save()
        return True, "success", vendor_location_serializer.data
    except Exception as e:
        print(f"[VendorLocationService Err] Failed to create vendor location: {e}")
        return False, "failed", None


def getVendorLocationDetailService(pk):
    try:
        obj = VendorLocation.objects.get(pk=pk)
        if obj:
            serializer = VendorLocationSerializer(instance=obj)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[VendorLocationService Err] Failed to get vendor location detail: {e}")
        return False, "failed", None


def updateVendorLocationDetailService(pk, link_token, requestData):
    try:
        print("absolute uri", requestData.build_absolute_uri())
        status = verify_location_capture_link(token=link_token, category="vendor")
        if not status:
            return False, "Invalid token", None

        # metadata, routes = prep_wegoo_location_data(requestData)

        obj = VendorLocation.objects.get(pk=pk)
        if obj:
            serializer = VendorLocationSerializer(
                instance=obj, data=requestData, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return True, "success", serializer.data
    except Exception as e:
        print(f"[VendorLocationService Err] Failed to update vendor location: {e}")
        return False, "failed", None


def deleteVendorLocationService(pk):
    try:
        obj = Vendor.objects.get(pk=pk)
        if obj:
            obj.delete()
        return True, "success", None
    except Exception as e:
        print(f"[VendorLocationService Err] Failed to delete vendor location: {e}")
        return False, "failed", None
