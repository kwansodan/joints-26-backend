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
    menuItem = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
              "id",
              "menuItem",
              "quantity",
        ]
    
    def get_menuItem(self, obj):
        if not hasattr(obj, "id"):
            return None 
        return obj.getMenuItem

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField(read_only=True)
    orderItems = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
              "id",
              "customer",
              "orderItems",
              "subtotal",
              # "location",
              # "status",
        ]

    def get_customer(self, obj):
        if not hasattr(obj, "id"):
            return None 
        return obj.getCustomer

    def get_orderItems(self, obj) -> list:
        if not hasattr(obj, "id"):
            return [] 
        return obj.orderItems



