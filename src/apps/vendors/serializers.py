from rest_framework import serializers
from src.apps.vendors.models import Vendor, Menu

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

    def get_menu(self, obj):
        if not hasattr(obj, "id"):
            return [] 
        return obj.menuList

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu 
        fields = [
              "id",
              "vendor",
              "name",
              "description",
              "price"
        ]

    
