from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from src.apps.orders.models import Location
from src.apps.orders.tasks import send_location_capture_link

@receiver(post_save, sender=Location)
def on_location_created(sender, instance: Location, created: bool, **kwargs):
    if created:
        order_id = f"send_location_capture_link-{instance.pk}"
        def _enqueue():
            send_location_capture_link.apply_async(
                args=(instance.pk,),
                task_id=order_id,
                retry=False
            )

        transaction.on_commit(_enqueue)
    else:
        print("location updated from signal. waiting on what to do...")

