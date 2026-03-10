from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.apps.bikers.models import Delivery
from src.apps.bikers.tasks import alert_vendor_on_order_delivery_created
from src.apps.orders.models import Order, OrderLocation
from src.services.server_sent_events import notify_frontend


@receiver(post_save, sender=Delivery)
def on_delivery_created(sender, instance: Delivery, created: bool, **kwargs):
    if created:
        delivery_id = f"alert_vendor_on_delivery_created-{instance.pk}"

        def _enqueue():
            alert_vendor_on_order_delivery_created.apply_async(
                args=(instance.pk,), task_id=delivery_id, retry=False
            )

        transaction.on_commit(_enqueue)
    else:
        print("delivery object updated")
