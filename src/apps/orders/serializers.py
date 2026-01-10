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
    class Meta:
        model = OrderItem
        fields = [
              "id",
              "menuItem",
              "quantity",
        ]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
              "id",
              "customer",
              "orderItem",
              "location",
              "subtotal",
              "status",
        ]

