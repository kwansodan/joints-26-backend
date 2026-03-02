from django.db import transaction

from src.apps.reports.models import Report
from src.apps.reports.serializers import ReportSerializer
from src.apps.users.models import User
from src.apps.users.serializers import AuthSerializer
from src.utils.helpers import clean_db_error_msgs


def reportssListService():
    try:
        objs = Report.objects.all()
        serializer = ReportSerializer(instance=objs, many=True)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[ReportService Err] Failed to get reports list: {e}")
        return False, "failed", None


def createReportService(user, requestData):
    try:
        data = dict(requestData.copy())
        data.update({"createdBy": user.id})
        report_serializer = ReportSerializer(data=data)
        report_serializer.is_valid(raise_exception=True)
        report_serializer.save()
        return True, "success", report_serializer.data 
    except Exception as e:
        print(f"[ReportService Err] Failed to create report : {e}")
        return False, "failed", None


def getReportDetailService(pk):
    try:
        obj = Report.objects.get(pk=pk)
        serializer = ReportSerializer(instance=obj)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[ReportService Err] Failed to get report detail: {e}")
        return False, "failed", None


def updateReportDetailService(pk, requestData):
    try:
        pass
    except Exception as e:
        print(f"[ReportService Err] Failed to update report: {e}")
        return False, "failed", None


def deleteReportService(pk):
    try:
        obj = Report.objects.get(pk=pk)
        obj.delete()
        return True, "success", None
    except Exception as e:
        print(f"[ReportService Err] Failed to delete report: {e}")
        return False, "failed", None
