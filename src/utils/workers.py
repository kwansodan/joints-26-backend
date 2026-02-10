from src.apps.external.models import GeneratedLink


def clean_email(data):
    chars = "abcdefghijklmnopqrstuvwxyz@.1234567890"
    data = str(data).lower()
    for i in data:
        if i not in chars:
            data = data.replace(i, "")
    return "".join(data)


def prep_wegoo_location_data(data: dict):
    try:
        assert isinstance(data, dict)
        metadata = {
            "country": data["country"],
            "destination": data["displayName"],
            "city": data["city"],
            "state": data["state"],
        }
        routes = {"latitude": data["latitude"], "longitude": data["longitude"]}
        return metadata, routes
    except Exception as e:
        print("Exception prepping wegoo metadata", str(e))
        return None, None


def verify_location_capture_link(token, category):
    assert isinstance(token, str), "Invalid link. Must be string instance"
    try:
        link = GeneratedLink.objects.filter(token=token, cateogry=category)
        return True if link.exists() else False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return
