from decimal import Decimal
from typing import Any

from rest_framework import serializers

from src.apps.orders.models import Location, Order, OrderItem
from src.apps.users.serializers import AuthSerializer
from src.apps.vendors.serializers import MenuItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    customerInfo = serializers.SerializerMethodField(read_only=True)
    subtotal = serializers.SerializerMethodField(read_only=True)
    menuItemsList = serializers.SerializerMethodField(read_only=True)
    locationData = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data):
        try:
            order = Order.objects.create(**validated_data)
            return order
        except Exception:
            return None

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "customerInfo",
            "menuItemsList",
            "subtotal",
            "locationData",
            "specialNotes",
            "deliveryStatus",
            "riderDispatched",
            "customerLocationCaptured",
        ]

    def get_customerInfo(self, obj) -> Any:
        try:
            return AuthSerializer(instance=obj.customer).data
        except:
            return None

    def get_menuItemsList(self, obj) -> Any:
        try:
            return OrderItemSerializer(
                instance=OrderItem.objects.filter(order=obj), many=True
            ).data
        except:
            return None

    def get_locationData(self, obj) -> Any:
        try:
            obj = Location.objects.get(order=obj)
            return LocationSerializer(instance=obj).data if obj else None
        except Exception as e:
            print("exception e", str(e))
            return None

    def get_subtotal(self, obj) -> Any:
        try:
            return sum(
                [
                    Decimal(item["menuItems"]["price"]) * item["quantity"]
                    for item in self.get_menuItemsList(obj)
                ]
            )
        except Exception:
            return 0.0


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
        ]

    def get_menuItems(self, obj) -> Any:
        try:
            return MenuItemSerializer(instance=obj.menuItem).data
        except Exception:
            return None


class LocationSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.captured = True
        return super().update(instance, validated_data)

    class Meta:
        model = Location
        fields = [
            "id",
            "order",
            "displayName",
            "latitude",
            "longitude",
            "state",
            "district",
            "city",
            "town",
            "suburb",
            "houseNumber",
            "captured",
            "road",
        ]
