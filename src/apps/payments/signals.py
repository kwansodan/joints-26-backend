from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.apps.payments.models import PaystackTransactionReference
from src.apps.payments.tasks import send_order_payment_link


@receiver(post_save, sender=PaystackTransactionReference)
def on_payment_transaction_ref_created(
    sender, instance: PaystackTransactionReference, created: bool, **kwargs
):
    if created:
        trxRefId = f"send_order_payment_link-{instance.pk}"

        def _enqueue():
            send_order_payment_link.apply_async(
                args=(instance.pk,), task_id=trxRefId, retry=False
            )

        transaction.on_commit(_enqueue)
    else:
        print("trxRef item updated...")
