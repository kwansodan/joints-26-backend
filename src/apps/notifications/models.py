from django.db import models
from src.utils.dbOptions import *
from src.apps.users.models import User
from src.utils.helpers import random_token

class Notification(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    notificationId = models.CharField(default=random_token, editable=False)
    sender = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, related_name="notification_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="notification_receiver")
    notificationType = models.CharField(max_length=MAX_STR_LEN, default="", choices=NOTIFICATION_TYPE, null=False, blank=False)
    topic = models.CharField(max_length=MAX_STR_LEN, null=True, blank=False)
    message = models.TextField(null=False)
    status = models.BooleanField(default=False)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class _Meta:
        verbose_name_plural = "Notification"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.notificationId} - {self.topic}, {self.status}"


