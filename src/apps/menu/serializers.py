from rest_framework import serializers
from src.apps.menu.models import Menu
from src.utils.dbOptions import MAX_STR_LEN 

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu 
        fields = [
              "id",
              "vendor",
              "name",
              "name",
              "description",
              "price",
        ]
