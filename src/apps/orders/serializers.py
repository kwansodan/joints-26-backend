from rest_framework import serializers
from src.apps.orders.models import Location, OrderItem, Order
from src.apps.users.models import User

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location 
        fields = [
              "id",
              "displayName",
              "latitude",
              "longitude",
              "region",
              "district",
              "city",
              "town",
              "suburb",
              "houseNumber",
              "road",
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    menuItems = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
              "id",
              "order",
              "menuItem",
              "menuItems",
              "quantity",
              "specialNotes",
        ]
    
    def get_menuItems(self, obj) -> list:
        if not hasattr(obj, "id"):
            return [] 
        return obj.getMenuItems

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField(read_only=True)
    subtotal = serializers.SerializerMethodField(read_only=True)
    menuItemsList = serializers.SerializerMethodField(read_only=True)
    locationData = serializers.SerializerMethodField(read_only=True)
    orderMetadata = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
              "id",
              "customer",
              "menuItemsList",
              "subtotal",
              "locationData",
              "orderMetadata",
              # "status",
        ]

    def get_customer(self, obj):
        if not hasattr(obj, "id"):
            return None 
        return obj.getCustomer

    def get_subtotal(self, obj) -> float:
        if not hasattr(obj, "id"):
            return 0.0
        return obj.orderSubtotal

    def get_menuItemsList(self, obj) -> list:
        if not hasattr(obj, "id"):
            return [] 
        return obj.menuItemsList

    def get_locationData(self, obj):
        if not hasattr(obj, "location") or not hasattr(obj, "id"):
            return None
        return obj.orderLocation

    def get_orderMetadata(self, obj) -> dict:
        return obj.orderMetadata

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
              "customer",
        ]

 
