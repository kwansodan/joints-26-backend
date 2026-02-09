from django.conf import settings
from celery import shared_task, Task
from src.utils.sms_mnotify import Mnotifiy
from src.apps.notifications.models import Notification

class BaseTaskWithRetry(Task):
    max_retries = 5
    default_retry_delay = 60

@shared_task(bind=True, base=BaseTaskWithRetry)
def send_notification(self, notification_id: str):
    try:
        notification = Notification.objects.get(pk=notification_id) 
    except Notification.DoesNotExist as e:
        raise self.retry(exc=e, countdown=60)
    
    if notification.processed:
        return {"status": "sms already sent", "notification_id": notification_id}

    recipients = [notification.recipient]
    message = notification.message

    try:
        mnotify = Mnotifiy(recipients=recipients, message=message)
        mnotify.send()
    except Exception as exc:
        raise self.retry(exc=exc)

    updated = Notification.objects.filter(pk=notification.pk, processed=False).update(processed=True)
    if updated == 0:
        return

    return {"status": "sms sent", "notification_id": notification_id}

