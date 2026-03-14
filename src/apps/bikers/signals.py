from pprint import pprint

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.apps.bikers.models import ChildDeliveryItem, ParentDeliveryItem
from src.apps.bikers.tasks import dispatch_order_delivery_wegoo
from src.utils.workers import prep_wegoo_delivery_price_detail


@receiver(post_save, sender=ParentDeliveryItem)
def onParentDeliveryCreated(
    sender, instance: ParentDeliveryItem, created: bool, **kwargs
):

    orderId = instance.orderId
    parent_delivery_id = instance.id
    dispatchService = getattr(instance, "dispatchService", "")
    task_id = f"dispatch_order_{orderId}-{parent_delivery_id}"

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

                is_delivery_fulfilment = False
                service = "intracity"

                # create sub delivery before dispatching to wegoo
                child_delivery_item, _ = ChildDeliveryItem.objects.get_or_create(
                    parentDeliveryItem=instance.id,
                )

                dispatch_order_delivery_wegoo.apply_async(
                    args=(
                        orderId,
                        parent_delivery_id,
                        child_delivery_item.id,
                        is_delivery_fulfilment,
                        service,
                        metadata,
                        item,
                    ),
                    task_id=task_id,
                    retry=False,
                )

        transaction.on_commit(_enqueue)

    else:
        print("delivery object updated")
