from rest_framework import serializers
from src.apps.payments.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment 
        fields = [
              "id",
              "paymentId",
              "order",
              "status",
              "amount",
              "paymentMethod",
              "paymentReference",
              "confirmedBy",
        ]

