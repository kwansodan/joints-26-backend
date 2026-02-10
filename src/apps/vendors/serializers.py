from typing import Any

from rest_framework import serializers

from src.apps.vendors.models import MenuItem, Vendor, VendorLocation


class VendorSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField(read_only=True)
    locations = serializers.SerializerMethodField(read_only=True)
    primaryLocation = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vendor
        fields = ["id", "user", "name", "locations", "primaryLocation", "phone", "menu"]

    def get_menu(self, obj) -> Any:
        if not hasattr(obj, "id"):
            return []
        return obj.menuList

    def get_locations(self, obj) -> Any:
        try:
            vendor_locations = VendorLocation.objects.filter(vendor=obj)
            return VendorLocationSerializer(instance=vendor_locations, many=True).data
        except Exception as e:
            print(f"Exception {str(e)}")
            return []

    def get_primaryLocation(self, obj) -> Any:
        try:
            primary_location = VendorLocation.objects.filter(vendor=obj).first()
            city = getattr(primary_location, "city", "N/A")
            return city if city else "N/A"
        except Exception as e:
            print(f"Exception {str(e)}")
            return "N/A"


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = [
            "id",
            "vendor",
            "name",
            "price",
            "description",
        ]


class VendorLocationSerializer(serializers.ModelSerializer):
    vendorInfo = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data):
        obj = VendorLocation.objects.create(**validated_data)
        return obj if obj else None 

    class Meta:
        model = VendorLocation
        fields = [
            "id",
            "vendor",
            "vendorInfo",
            "displayName",
            "latitude",
            "longitude",
            "city",
            "state",
            "houseNumber",
            "road",
            "town",
            "suburb",
            "district",
            "captured"
        ]

    def get_vendorInfo(self, obj) -> Any:
        try:
            vendor = Vendor.objects.get(id=obj.vendor.id)
            return {"name": vendor.name, "phone": vendor.phone, "captured": obj.captured}
        except Exception as e:
            print(f"Exception {str(e)}")
            return None
