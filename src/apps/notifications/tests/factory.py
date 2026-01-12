from django.contrib.auth import get_user_model
from src.apps.notifications.models import Notification

User = get_user_model()

def create_nofitication(
    sender: User,
    receiver: User,
    topic="New Topic",
    message="New topic message",
    notificationType="sms"
    ):
    notification = Notification.objects.create(
        sender=sender,
        receiver=receiver,
        topic=topic,
        message=message,
        notificationType=notificationType

    )
    return notification  


