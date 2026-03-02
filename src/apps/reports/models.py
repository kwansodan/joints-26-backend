
from django.db import models

from src.utils.dbOptions import *
from src.utils.helpers import random_token

class Report(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    reportId = models.CharField(default=random_token, null=False, blank=False, editable=False)
    reportName = models.CharField(max_length=MAX_STR_LEN, null=False, blank=False)
    reportName = models.CharField(max_length=MAX_STR_LEN, null=False, blank=False)
    exportFormat = models.CharField(max_length=TINY_STR_LEN, choices=REPORT_EXPORT_FORMAT, default="pdf", null=False, blank=False)
    reportType = models.CharField(
        max_length=MAX_STR_LEN, choices=REPORT_TYPES, null=False, blank=False
    )
    reportScope = models.CharField(
        max_length=MAX_STR_LEN, choices=REPORT_SCOPE, null=False, blank=False
    )
    reportNotes = models.TextField(null=True, blank=True)
    createdBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    updatedBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class _Meta:
        verbose_name_plural = "Reports"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"Report - {self.reportId}"
