from rest_framework import serializers
from src.apps.vendors.models import Vendor, MenuItem

class VendorSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vendor 
        fields = [
              "id",
              "user",
              "name",
              "location",
              "phone",
              "menu"
        ]

    def get_menu(self, obj) -> list:
        if not hasattr(obj, "id"):
            return [] 
        return obj.menuList

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

    
