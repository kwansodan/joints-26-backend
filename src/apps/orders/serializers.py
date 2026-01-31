from rest_framework import serializers
from src.apps.orders.models import Location, OrderItem, Order

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
    
    def get_menuItems(self, obj):
        if not hasattr(obj, "id"):
            return None 
        return obj.getMenuItems

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField(read_only=True)
    menuItemsList = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
              "id",
              "customer",
              "menuItemsList",
              "subtotal",
              # "location",
              # "status",
        ]

    def get_customer(self, obj):
        if not hasattr(obj, "id"):
            return None 
        return obj.getCustomer

    def get_menuItemsList(self, obj) -> list:
        if not hasattr(obj, "id"):
            return [] 
        return obj.menuItemsList

class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
              "customer",
        ]

 
