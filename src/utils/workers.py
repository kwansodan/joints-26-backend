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


def prep_wegoo_location_data(order_location_id: str):
    try:
        assert isinstance(order_location_id, str), "order not a str instance"

        try:
            destination = Location.objects.get(id=order_location_id)
        except Location.DoesNotExist:
            return False, {}

        order = destination.order
        order_vendors = order.vendorLocation
        print("order vendors", order_vendors)

        return True, {
            "destination_country": "Ghana",
            "destination": "Grand Floor & 1st Floor , P-Cular Heights behind Legon U.P.S.A Madina, New Rd, Accra, Ghana",
            "destination_city": "Accra",
            "destination_state": "Greater Accra",
            "origin_country": "Ghana",
            "origin": "JRWV+XR4, East Legon, Accra Ghana",
            "origin_city": "Accra",
            "origin_state": "Greater Accra",
            "routes": {
                "origin": {"latitude": 5.64791, "longitude": -0.15562},
                "destination": {"latitude": 5.666179800000001, "longitude": -0.164801},
            },
        }
    except Exception as e:
        print("Exception prepping wegoo metadata", str(e))
        return False, None
