from rest_framework import serializers
from src.apps.bikers.models import Biker, Vehicle

class BikerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biker 
        fields = [
              "id",
              "user",
              "status",
              "totalTrips",
        ]

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
