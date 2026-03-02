from django.urls import path

from src.apps.reports.views.report import *

app_name = "reports"

urlpatterns = [
    path("", ReportListView.as_view(), name="report-list-view"),
    path("detail/<str:pk>/", ReportDetailView.as_view(), name="report-detail-view"),
]
