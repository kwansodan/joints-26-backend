from rest_framework import serializers

from src.apps.payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "paymentStatus",
            "amount",
            "processed",
            "paymentMethod",
            "paymentReference",
            "confirmedBy",
        ]

    def create(self, validated_data):
        try:
            payment = Payment.objects.create(**validated_data)
            return payment
        except Exception as e:
            print("exception", str(e))
            return None

    def get_amount(self, obj):
        if not hasattr(obj, "order"):
            return 0.0
        return obj.order.subtotal
