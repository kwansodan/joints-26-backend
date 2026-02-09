from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from src.apps.payments.models import Payment
from src.apps.payments.tasks import send_order_payment_link

@receiver(post_save, sender=Payment)
def on_payment_created(sender, instance: Payment, created: bool, **kwargs):
    if not created:
        return

    order_id = f"send_order_payment_link-{instance.pk}"

    def _enqueue():
        send_order_payment_link.apply_async(
            args=(instance.pk,),
            task_id=order_id,
            retry=False
        )

    transaction.on_commit(_enqueue)
