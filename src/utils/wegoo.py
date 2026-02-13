from pprint import pprint

import requests
from django.conf import settings
from django.utils import timezone

API_KEY = settings.WEGOO_API_KEY


class WeGoo:
    def __init__(
        self,
        is_fulfillment_delivery=False,
        service="intracity",
        details={},
        currency="GHS",
        delivery_option="SAME_DAY",
        send_notifications=False,
        webhook_url="",
        is_pickup=True,
        is_prepaid_delivery=True,
        recipient={},
        sender={},
    ):
        self.is_fulfilment_delivery = is_fulfillment_delivery
        self.service = service
        self.details = details
        self.currency = currency
        self.delivery_option = delivery_option
        self.send_notification = send_notifications
        self.webhook_url = webhook_url
        self.is_pickup = is_pickup
        self.is_prepaid_delivery = is_prepaid_delivery
        self.pick_up_at = self._get_pickup_time()
        self.recipient = recipient
        self.sender = sender
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        self.get_quote_url = "https://api.wegoo.delivery/v1/deliveries/price"
        self.create_delivery_url = "https://api.wegoo.delivery/v1/deliveries"

    def _get_pickup_time(self):
        delta = timezone.now() + timezone.timedelta(hours=2)
        return delta.isoformat()

    def validate(self):
        if self.service not in ["intracity", "nationwide"]:
            raise ValueError("Invalid service type")

        if self.currency not in ["GHS"]:
            raise ValueError("Invalid currency")

        if self.details is None:
            raise TypeError("details cannot be None")

        # recipient & sender
        if not isinstance(self.recipient, dict) or not isinstance(self.sender, dict):
            raise TypeError("Invalid recipient and sender data")

        for field in ["name", "phone"]:
            if field not in self.sender or field not in self.recipient:
                raise KeyError("missing recipient or sender field")

        # details
        if not isinstance(self.details, dict):
            raise TypeError("details must be a dict")

        # items
        if "items" not in self.details or "routes" not in self.details:
            raise KeyError("items or routes field is required")

        if len(self.details["items"]) < 1:
            raise ValueError("no items provided")

        for _, value in self.details.items():
            if value is None:
                raise TypeError("Invalid details data")

        for item in self.details["items"]:
            for key, value in item.items():
                if key not in [
                    "name",
                    "type",
                    "add_insurance",
                    "quantity",
                    "price",
                    "weight",
                    "is_fragile",
                ]:
                    raise KeyError(f"{key} missing in order item info")

        # routes
        if (
            "origin" not in self.details["routes"]
            or not "destination" in self.details["routes"]
        ):
            raise KeyError("missing orgin or destination routes")

        for _, value in self.details["routes"]["destination"].items():
            if value is None or type(value) is not float:
                raise ValueError("Invalid destination route data")

        for _, value in self.details["routes"]["origin"].items():
            if value is None or type(value) is not float:
                raise ValueError("Invalid origin route data")

        if self.details["destination_country"] != self.details["origin_country"]:
            raise ValueError(
                "only nationwide delivery supported now. Use same country for destination and origin"
            )

    def create_quote(self):
        self.validate()

        self.service = (
            "nationwide"
            if self.details["destination_state"] != self.details["origin_state"]
            else "intracity"
        )

        self.delivery_option = "SAME_DAY" if self.service == "intracity" else "NEXT_DAY"

        data = {
            "is_fulfillment_delivery": self.is_fulfilment_delivery,
            "service": self.service,
            "details": [self.details],
        }

        # pprint(data, indent=1)

        try:
            response = requests.post(
                url=self.get_quote_url, json=data, headers=self.headers
            )
            # print("quote response", response.json())

            if response.status_code in [201, 200]:
                result = response.json()
                quote_data = [result["data"][0]]
                return True, quote_data
            else:
                return False, None
        except Exception as e:
            print(f"[WeGoo Create Delivery Price Exception]: {str(e)}")
            return False, None

    def create_delivery(self):
        quote_status, quote_data = self.create_quote()
        print("quote data", quote_data)

        if not quote_status or not quote_data:
            return False

        try:
            for index, item in enumerate(quote_data):
                self.details["items"][index].pop("add_insurance")
                data = {
                    "currency": self.currency,
                    "delivery_option": self.delivery_option,
                    "is_fulfillment_delivery": self.is_fulfilment_delivery,
                    "send_notifications": self.send_notification,
                    "webhook_url": self.webhook_url,
                    "quote_id": item["quote_id"],
                    "is_pickup": self.is_pickup,
                    "deliveries": [
                        {
                            "destination": self.details["destination"],
                            "destination_country": self.details["destination_country"],
                            "destination_state": self.details["destination_state"],
                            "destination_city": self.details["destination_city"],
                            "destination_country_code": "GH",
                            "origin": self.details["origin"],
                            "origin_city": self.details["origin_city"],
                            "origin_country": self.details["origin_country"],
                            "origin_state": self.details["origin_state"],
                            "origin_country_code": "GH",
                            "is_prepaid_delivery": self.is_prepaid_delivery,
                            "items": self.details["items"],
                            "pick_up_at": self.pick_up_at,
                            "route": {
                                "origin": self.details["routes"]["origin"],
                                "destination": self.details["routes"]["destination"],
                            },
                            "recipient": self.recipient,
                            "sender": self.sender,
                            "service": self.service,
                        },
                    ],
                }

            pprint(data, indent=1)

            response = requests.post(
                url=self.create_delivery_url, json=data, headers=self.headers
            )
            print("response from create delivery", response.json())

            if response.status_code in [201, 200]:
                print("\n delivery response\n", response)
                return (True,)
            else:
                return False
        except Exception as e:
            print(f"[WeGoo Create Delivery Price Exception]: {str(e)}")
            return False
