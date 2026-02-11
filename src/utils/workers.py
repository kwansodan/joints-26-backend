from src.apps.external.models import GeneratedLink
from src.apps.orders.models import Location, Order


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
        return


def prep_wegoo_location_data(order_id: str):
    wegoo_location_pairs = []
    try:
        assert isinstance(order_id, str), "order_location_id not a str instance"

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return False, None

        destination_obj = order.location

        orderitems = order.orderitem_set.all()
        for item in orderitems:
            print(item.menuItem.vendor.location.__dict__)
            origin_obj = item.menuItem.vendor.location

            wegoo_location_pairs.append(
                {
                    "destination_country": destination_obj.country,
                    "destination": destination_obj.displayName,
                    "destination_city": destination_obj.city,
                    "destination_state": destination_obj.state,
                    "origin_country": origin_obj.country,
                    "origin": origin_obj.displayName,
                    "origin_city": origin_obj.city,
                    "origin_state": origin_obj.state,
                    "routes": {
                        "origin": {
                            "latitude": origin_obj.latitude,
                            "longitude": origin_obj.longitude,
                        },
                        "destination": {
                            "latitude": origin_obj.latitude,
                            "longitude": origin_obj.longitude,
                        },
                    },
                }
            )
        return True, wegoo_location_pairs
    except Exception as e:
        print("Exception prepping wegoo metadata", str(e))
        return False, None
