from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from src.apps.notifications.models import Notification
from src.apps.notifications.tasks import send_notification

@receiver(post_save, sender=Notification)
def on_notification_created(sender, instance: Notification, created: bool, **kwargs):
    if not created:
        return

    notification_id = f"send_notification-{instance.pk}"

    def _enqueue():
        send_notification().apply_async(
            args=(instance.pk,),
            task_id=notification_id,
            retry=False
        )

    transaction.on_commit(_enqueue)
