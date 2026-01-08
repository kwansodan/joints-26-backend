from rest_framework import serializers
from src.apps.bikers.models import Biker, BikerVehicle
from src.utils.dbOptions import MAX_STR_LEN 

class BikerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biker 
        fields = [
              "id",
              "user",
              "status",
              "totalTrips",
        ]

class BikerVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikerVehicle
        fields = [
              "id",
              "biker",
              "vehicleType",
              "licensePlate",
        ]
