from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.apps.orders.models import Order, OrderLocation
from src.apps.orders.tasks import send_order_location_capture_link
from src.services.server_sent_events import notify_frontend


@receiver(post_save, sender=OrderLocation)
def on_location_created(sender, instance: OrderLocation, created: bool, **kwargs):
    if created:
        order_id = f"send_order_location_capture_link-{instance.pk}"

        def _enqueue():
            send_order_location_capture_link.apply_async(
                args=(instance.pk,), task_id=order_id, retry=False
            )

        transaction.on_commit(_enqueue)
    else:

        def _update_order_location():
            try:
                updated = Order.objects.filter(
                    id=instance.order.id, 
                ).update(customerLocationCaptured=instance.captured)
                if updated > 0:
                    print(
                        "updated made. can call wegoo task delivery here. agreed to be triggered by agent"
                    )
                else:
                    return
            except Exception as e:
                print("order location updated signal exception", str(e))

        transaction.on_commit(_update_order_location)
        customer = instance.order.customer
        if customer is not None:
            customer_fullname = f"{customer.first_name} {customer.last_name}"
            notify_frontend(
                update_type="Order",
                update_action="location",
                update_id=f"{customer_fullname}",
                status=instance.captured,
            )

