from src.apps.orders.models import Order
from src.apps.vendors.models import Vendor, VendorLocation
from src.apps.vendors.serializers import VendorLocationSerializer
from src.utils.wegoo import WeGoo
from src.utils.workers import (
    prep_wegoo_delivery_price_detail,
    verify_location_capture_link,
)


def updateOrderRiderDispatchService(pk, requestData):
    try:
        order = Order.objects.get(id=pk)

        if not order.customerLocationCaptured:
            return False, "customer location not captured", None

        if order.riderDispatched:
            return True, "success", None

        prep_status, delivery_price_detail = prep_wegoo_delivery_price_detail(
            order_id=pk
        )
        if not prep_status or delivery_price_detail is None:
            return False, "Failed to prep wegoo delivery price detail", None

        for item in delivery_price_detail:
            metadata = item.pop("metadata")
            wegoo = WeGoo(
                is_fulfillment_delivery=False,
                service="nationwide",
                details=item,
                recipient=metadata["recipient"],
                sender=metadata["sender"],
            )
            delivery_status = wegoo.create_delivery()
            if not delivery_status:
                print("DELIVERY CREATION FAILED")
                return False, "failed to create delivery price", None
        return True, "success", None
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
