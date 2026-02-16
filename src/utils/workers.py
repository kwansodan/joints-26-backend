from src.apps.external.models import GeneratedLink
from src.apps.orders.models import OrderLocation, Order


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
        link = GeneratedLink.objects.filter(token=token, category=category)
        return True if link.exists() else False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False


def prep_wegoo_delivery_price_detail(order_id: str):
    try:
        assert isinstance(order_id, str), "order_location_id not a str instance"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return False, None

        destination_obj = order.orderlocation

        orderitems = order.orderitem_set.all()
        wegoo_delivery_objs = [{}] * len(orderitems)

        for index, item in enumerate(orderitems):
            vendor = item.menuItem.vendor
            origin_obj = item.menuItem.vendor.location

            wegoo_delivery_objs[index].update(
                {
                    "destination_country": destination_obj.country or "Ghana",
                    "destination": destination_obj.displayName,
                    "destination_city": destination_obj.city,
                    "destination_state": destination_obj.state,
                    "origin_country": origin_obj.country or "Ghana",
                    "origin": origin_obj.displayName,
                    "origin_city": origin_obj.city,
                    "origin_state": origin_obj.state,
                    "routes": {
                        "origin": {
                            "latitude": float(origin_obj.latitude),
                            "longitude": float(origin_obj.longitude),
                        },
                        "destination": {
                            "latitude": float(origin_obj.latitude),
                            "longitude": float(origin_obj.longitude),
                        },
                    },
                    "items": [
                        {
                            "name": item.menuItem.name,
                            "type": "Food",
                            "add_insurance": False,
                            "quantity": item.quantity,
                            "price": float(item.menuItem.price),
                            "weight": 1,
                            "is_fragile": True,
                        }
                    ],
                    "metadata": {
                        "recipient": {
                            "name": f"{order.customer.get_full_name()}",
                            "phone": order.customer.phone,
                        },
                        "sender": {"name": vendor.name, "phone": vendor.phone},
                    },
                }
            )
        return True, wegoo_delivery_objs
    except Exception as e:
        print("Exception prepping wegoo metadata", str(e))
        return False, None
