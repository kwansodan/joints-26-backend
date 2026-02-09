from rest_framework import serializers
from src.apps.notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification 
        fields = [
              "id",
              "recipient",
              "message",
              "processed",
        ]

