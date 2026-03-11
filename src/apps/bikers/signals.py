from pprint import pprint

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.apps.bikers.models import Delivery
from src.apps.bikers.tasks import alert_vendor_on_order_delivery_created, dispatch_order_delivery_wegoo
from src.utils.wegoo import WeGoo
from src.utils.workers import prep_wegoo_delivery_price_detail


@receiver(post_save, sender=Delivery)
def on_delivery_created(sender, instance: Delivery, created: bool, **kwargs):

    delivery_task_id = f"alert_vendor_on_delivery_created-{instance.pk}"
    orderId = instance.orderId
    dispatchService = getattr(instance, "dispatchService", "")

    if created:

        def _enqueue():
            prep_status, delivery_price_detail = prep_wegoo_delivery_price_detail(
                order_id=orderId
            )
            # print("FILTERED", filtered_delivery_objs)

            if not prep_status or delivery_price_detail is None:
                print("PRICE CREATION FAILED")
                return False

            filtered_delivery_objs = []
            for item in delivery_price_detail:
                [filtered_delivery_objs.append(v) for _, v in item.items()]

            for item in filtered_delivery_objs:
                metadata = item.pop("metadata")

                dispatch_order_delivery_wegoo.apply_async(
                    args=(instance.pk,), task_id=delivery_task_id, retry=False
                )
                wegoo = WeGoo(
                    is_fulfillment_delivery=False,
                    service="intracity",
                    details=filtered_delivery_objs,
                    recipient=metadata["recipient"],
                    sender=metadata["sender"],
                )

                # delivery_status, tracking_number, delivery_type = (
                #     wegoo.create_delivery()
                # )
                # if not delivery_status:
                #     print("DELIVERY CREATION FAILED")
                #     return False, "failed to create delivery price", None

            # Delivery.objects.filter(
            #     orderId=orderId, dispatchService=dispatchService
            # ).update(
            #     dispatchServiceTrackingNumber=tracking_number,
            #     dispatchServiceDeliveryType=delivery_type,
            # )
            #
            #     alert_vendor_on_order_delivery_created.apply_async(
            #         args=(instance.pk,), task_id=delivery_task_id, retry=False
            #     )

        transaction.on_commit(_enqueue)

    else:
        print("delivery object updated")
