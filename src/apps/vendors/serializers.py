from rest_framework import serializers
from src.apps.vendors.models import Vendor
from django.contrib.auth.hashers import make_password

class VendorSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vendor 
        fields = [
              "id",
              "name",
              "location",
              "phone",
              "menu"
        ]

    def get_menu(self, obj):
        if not hasattr(obj, "id"):
            return [] 
        return obj.menuList


