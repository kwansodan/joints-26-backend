from pprint import pprint

from django.db import transaction

from src.apps.bikers.models import ParentDeliveryItem
from src.apps.bikers.tasks import alert_vendor_on_order_delivery_created
from src.apps.orders.models import Order
from src.utils.wegoo import WeGoo
from src.utils.workers import prep_wegoo_delivery_price_detail


def updateOrderRiderDispatchService(pk, requestData):
    dispatchService = requestData.get("dispatchService")
    print("request data", requestData)
    print("dispatch service", dispatchService)

    try:
        with transaction.atomic():
            order = Order.objects.get(id=pk)
            orderLocation = order.orderlocation
            paymentObj = order.payment

            if order.riderDispatched:
                return True, "Rider has already been dispatched", None

            if not orderLocation or not paymentObj:
                return False, "Customer order location or payment not found", None

            if not orderLocation.captured:
                return False, "Customer location must be captured to proceed", None

            if not paymentObj.processed or not paymentObj.paymentStatus:
                return False, "Payment must be made to proceed", None

            deliveryObj, created = ParentDeliveryItem.objects.get_or_create(
                orderId=order.id, dispatchService=dispatchService
            )
            if not created:
                if deliveryObj.all_childDeliveriesProcessed:
                    return (
                        True,
                        "Delivery has already been assigned and vendor notified",
                        None,
                    )
                else:
                    deliveryObj.delete()
                    ParentDeliveryItem.objects.create(
                        orderId=order.id, dispatchService=dispatchService
                    )
            return True, "Successfully dispatched rider for this order", None

            # else:
            #     prep_status, delivery_price_detail = prep_wegoo_delivery_price_detail(
            #         order_id=pk
            #     )
            #     if not prep_status or delivery_price_detail is None:
            #         return False, "Failed to prep wegoo delivery price detail", None
            #
            #     for item in delivery_price_detail:
            #         metadata = item.pop("metadata")
            #
            #         wegoo = WeGoo(
            #             is_fulfillment_delivery=False,
            #             service="intracity",
            #             details=item,
            #             recipient=metadata["recipient"],
            #             sender=metadata["sender"],
            #         )
            #         delivery_status, tracking_number, delivery_type = (
            #             wegoo.create_delivery()
            #         )
            #         if not delivery_status:
            #             print("DELIVERY CREATION FAILED")
            #             return False, "failed to create delivery price", None
            #
            #         Delivery.objects.create(
            #             orderId=order.id,
            #             dispatchServiceTrackingNumber=tracking_number,
            #             dispatchServiceDeliveryType=delivery_type,
            #             dispatchService=dispatchService,
            #         )
            # return True, "success", None
    except Exception as e:
        print(f"[WegooOrderDispatchService Err] Failed to dispatch wegoo order: {e}")
        return False, "failed", None


"""
{
  "currency": "GHS",
  "delivery_option": "SAME_DAY",
  "is_fulfillment_delivery": false,
  "send_notifications": false,
  "webhook_url": "https://eosjeb3aa04jvt7.m.pipedream.net",
  "quote_id": "691e08331ac6dfdb348e06b5",
  "is_pickup": true,
  "deliveries": [
    {

      # HAVE THIS
      "destination": "Grand Floor & 1st Floor , P-Cular Heights behind Legon U.P.S.A Madina, New Rd, Accra, Ghana",
      "destination_country": "Ghna",
      "destination_state": "Greater Accra",
      "destination_city": "Accra",
      "destination_country_code": "GH",
      "is_prepaid_delivery": false,
      "items": [
        {
          "name": "Test",
          "type": "Electronics",
          "quantity": 1,
          "price": 500,
          "weight": 1,
          "is_fragile": false
        }
      ],
      "origin": "JRWV+XR4, East Legon, Accra Ghana",
      "origin_city": "Accra",
      "origin_country": "Ghana",
      "origin_country_code": "GH",
      "origin_state": "Greater Accra",

      "payload": null,

      "pick_up_at": "2025-11-20T11:26:25.127Z",

      # HAVE THIS
      "route": {
        "origin": {
          "latitude": 5.64791,
          "longitude": -0.15562
        },
        "destination": {
          "latitude": 5.666179800000001,
          "longitude": -0.164801
        }
      },

      "recipient": {
        "name": "Jane",
        "phone": "+233558343508"
      },

      "sender": {
        "name": "Hasnem Fabrics",
        "phone": "+233558343508"
      },

      "service": "intracity"

    }
  ]
}


"""
