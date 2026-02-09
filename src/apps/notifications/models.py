from django.db import models
from src.utils.dbOptions import *
from src.utils.helpers import random_token

class Notification(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    recipient = models.CharField(max_length=TINY_STR_LEN, null=True, blank=False)
    message = models.TextField(null=False)
    processed = models.BooleanField(default=False)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "Notification"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.recipient} - {self.processed}"


