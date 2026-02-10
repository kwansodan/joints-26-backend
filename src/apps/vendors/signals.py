from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.apps.vendors.models import VendorLocation
from src.apps.vendors.tasks import send_vendor_location_capture_link


@receiver(post_save, sender=VendorLocation)
def on_vendorLocation_created(
    sender, instance: VendorLocation, created: bool, **kwargs
):
    if created:
        order_id = f"send_vendor_location_capture_link-{instance.pk}"

        def _enqueue():
            send_vendor_location_capture_link.apply_async(
                args=(instance.pk,), task_id=order_id, retry=False
            )

        transaction.on_commit(_enqueue)
    else:
        print("location updated")
