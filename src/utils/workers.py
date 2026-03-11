from pprint import pprint

from src.apps.external.models import GeneratedLink
from src.apps.orders.models import Order, OrderLocation


def clean_email(data):
    chars = "abcdefghijklmnopqrstuvwxyz@.1234567890"
    data = str(data).lower()
    for i in data:
        if i not in chars:
            data = data.replace(i, "")
    return "".join(data)


def verify_location_capture_link(token, category):
    assert isinstance(token, str), "Invalid link. Must be string instance"
    try:
        link = GeneratedLink.objects.get(token=token, category=category)
        if link is not None and not link.expired:
            return True
        else:
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False


def prep_wegoo_delivery_price_detail(order_id: str):
    try:
        assert isinstance(order_id, str), "order_location_id not a str instance"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return False, []

        destination_obj = order.orderlocation
        orderitems = order.orderitem_set.all()

        unique_origins = set(
            [str(item.menuItem.vendor.location.displayName) for item in orderitems]
        )
        unique_origins_struct = [{f"{item}": {"items": [], "metadata": {}}} for item in unique_origins]

        location_keys = ["_country", "_city", "_state", ""]
        destination_keys = [f"destination{item}" for item in location_keys]
        origin_keys = [f"origin{item}" for item in location_keys]

        for _, item in enumerate(orderitems):
            vendor = item.menuItem.vendor
            vendor_location = item.menuItem.vendor.location
            vendor_location_displayName = vendor_location.displayName

            currentItem = {
                "name": item.menuItem.name,
                "type": "Food",
                "add_insurance": False,
                "quantity": item.quantity,
                "price": float(item.menuItem.price),
                "weight": 1,
                "is_fragile": True,
            }

            currentLocationData = {
                "destination_country": destination_obj.country or "Ghana",
                "destination": destination_obj.displayName,
                "destination_city": destination_obj.city,
                "destination_state": destination_obj.state,
                "origin_country": vendor_location.country or "Ghana",
                "origin": vendor_location.displayName,
                "origin_city": vendor_location.city,
                "origin_state": vendor_location.state,
                "routes": {
                    "origin": {
                        "latitude": float(vendor_location.latitude),
                        "longitude": float(vendor_location.longitude),
                    },
                    "destination": {
                        "latitude": float(destination_obj.latitude),
                        "longitude": float(destination_obj.longitude),
                    },
                },
            }

            currentMetaData = {
                "recipient": {
                    "name": f"{order.customer.customer_fullname}",
                    "phone": order.customer.phone,
                },
                "sender": {"name": vendor.name, "phone": vendor.phone},
            }

            for q in unique_origins_struct:
                if vendor_location_displayName in q:
                    struct_item = q[f"{vendor_location_displayName}"]

                    # destination
                    if destination_keys != list(struct_item.keys()):
                        for dkey in destination_keys:
                            struct_item.update(
                                {f"{dkey}": currentLocationData[f"{dkey}"]}
                            )

                    # origin
                    if origin_keys != list(struct_item.keys()):
                        for okey in origin_keys:
                            struct_item.update(
                                {f"{okey}": currentLocationData[f"{okey}"]}
                            )

                    # routes
                    if "routes" not in struct_item:
                        struct_item.update({"routes": currentLocationData["routes"]})

                    # main order items
                    struct_item["items"].append(currentItem)
                    struct_item["metadata"] = currentMetaData

            # currentQuote = {
            #     "destination_country": destination_obj.country or "Ghana",
            #     "destination": destination_obj.displayName,
            #     "destination_city": destination_obj.city,
            #     "destination_state": destination_obj.state,
            #     "origin_country": vendor_location.country or "Ghana",
            #     "origin": vendor_location.displayName,
            #     "origin_city": vendor_location.city,
            #     "origin_state": vendor_location.state,
            #     "routes": {
            #         "origin": {
            #             "latitude": float(vendor_location.latitude),
            #             "longitude": float(vendor_location.longitude),
            #         },
            #         "destination": {
            #             "latitude": float(destination_obj.latitude),
            #             "longitude": float(destination_obj.longitude),
            #         },
            #     },
            #     "items": [
            #         {
            #             "name": item.menuItem.name,
            #             "type": "Food",
            #             "add_insurance": False,
            #             "quantity": item.quantity,
            #             "price": float(item.menuItem.price),
            #             "weight": 1,
            #             "is_fragile": True,
            #         }
            #     ],
            #     "metadata": {
            #         "recipient": {
            #             "name": f"{order.customer.customer_fullname}",
            #             "phone": order.customer.phone,
            #         },
            #         "sender": {"name": vendor.name, "phone": vendor.phone},
            #     },
            # }
            #
            # for q in unique_origins_struct:
            #     if vendor_location_displayName in q:
            #         q[f"{vendor_location_displayName}"].append(currentQuote)
            #
        # pprint(unique_origins_struct)
        # for uqitem in unique_origins_struct:
        #     pass

        return True, unique_origins_struct
    except Exception as e:
        print("Exception prepping wegoo metadata", str(e))
        return False, []
