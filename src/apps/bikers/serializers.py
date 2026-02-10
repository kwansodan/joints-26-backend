from typing import Any
from rest_framework import serializers
from src.apps.bikers.models import Biker, Vehicle

class BikerSerializer(serializers.ModelSerializer):
    userInfo = serializers.SerializerMethodField(read_only=True)
    vehicles = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Biker 
        fields = [
              "id",
              "user",
              "userInfo",
              "status",
              "totalTrips",
              "vehicles"
        ]

    def get_vehicles(self, obj) -> Any:
        return obj.vehicles

    def get_userInfo(self, obj) -> Any:
        return obj.userInfo


class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = [
              "id",
              "biker",
              "vehicleType",
              "licensePlate",
              "registered",
        ]
