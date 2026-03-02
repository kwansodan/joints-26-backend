from rest_framework import serializers
from typing import Any

from src.apps.reports.models import Report
from src.apps.users.models import User


class ReportSerializer(serializers.ModelSerializer):
    createdByName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Report
        fields = [
            "id",
            "reportId",
            "reportName",
            "reportType",
            "reportScope",
            "reportNotes",
            "exportFormat",
            "createdBy",
            "createdAt",
            "createdByName",
        ]
    
    def get_createdByName(self, obj) -> Any:
        if not hasattr(obj, "createdBy"):
            return "---"
        if obj.createdBy != "dev":
            user = User.objects.get(id=obj.createdBy)
            return user.get_full_name()
        else:
            return obj.createdBy


