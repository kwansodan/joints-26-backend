from decimal import Decimal
from typing import Any

from rest_framework import serializers

from src.apps.orders.models import Order, OrderItem, OrderLocation
from src.apps.payments.models import Payment
from src.apps.users.serializers import CustomerSerializer
from src.apps.vendors.serializers import MenuItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    customerInfo = serializers.SerializerMethodField(read_only=True)
    subtotal = serializers.SerializerMethodField(read_only=True)
    menuItemsList = serializers.SerializerMethodField(read_only=True)
    locationData = serializers.SerializerMethodField(read_only=True)
    paymentLinkSent = serializers.SerializerMethodField(read_only=True)
    paymentLink = serializers.SerializerMethodField(read_only=True)
    paymentInfo = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data):
        try:
            order = Order.objects.create(**validated_data)
            if order:
                Payment.objects.create(order=order)
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
            "paymentConfirmed",
            "deliveryStatus",
            "riderDispatched",
            "customerLocationCaptured",
            "paymentLinkSent",
            "paymentLink",
            "paymentInfo",
        ]

    def get_customerInfo(self, obj) -> Any:
        try:
            return CustomerSerializer(instance=obj.customer).data
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
            obj = OrderLocation.objects.get(order=obj)
            return OrderLocationSerializer(instance=obj).data if obj else None
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

    def get_paymentLinkSent(self, obj) -> Any:
        return True if obj.paystackTrxRefObj.processed else False

    def get_paymentLink(self, obj) -> Any:
        if obj.paystackTrxRefObj:
            return obj.paystackTrxRefObj.paymentLink
        return "N/A"

    def get_paymentInfo(self, obj) -> Any:
        if not obj.payment or not obj.paystackTrxRefObj:
            return None
        paymentObj = obj.payment
        return {
            "paid_at": paymentObj.paid_at,
            "channel": paymentObj.paymentMethod,
            "receipt_number": paymentObj.receipt_number,
        }

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


class OrderLocationSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.captured = True
        return super().update(instance, validated_data)

    class Meta:
        model = OrderLocation
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
