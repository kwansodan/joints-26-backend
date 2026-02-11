import requests
from django.conf import settings

API_KEY = settings.WEGOO_API_KEY

"""
"is_fulfillment_delivery": false,
 "service": "intracity",
 "details": [
  {
   "destination_country": "Ghana",
   "destination": "Grand Floor & 1st Floor , P-Cular Heights behind Legon U.P.S.A Madina, New Rd, Accra, Ghana",
   "destination_city": "Accra",
   "destination_state": "Greater Accra",
   "origin_country": "Ghana",
   "origin": "JRWV+XR4, East Legon, Accra Ghana",
   "origin_city": "Accra",
   "origin_state": "Greater Accra",
   "routes": {
    "origin": {
     "latitude": 5.64791,
     "longitude": -0.15562
    },
    "destination": {
     "latitude": 5.666179800000001,
     "longitude": -0.164801
    }
   },
   "items": [
    {
     "name": "Iphone",
     "type": "Books & Stationery",
     "add_insurance": false,
     "quantity": 1,
     "price": 1,
     "weight": 1,
     "is_fragile": false
    }
   ]
  }
 ]

"""


class WeGoo:
    def __init__(
        self,
        is_fulfillment_delivery=False,
        service="intracity",
        details={},
    ):
        self.is_fulfilment_delivery = is_fulfillment_delivery
        self.service = service
        self.details = details
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        self.create_delivery_price_url = (
            "https://api.wegoo.delivery/v1/deliveries/price"
        )

    def validate(self):
        if self.details is None:
            raise TypeError("details cannot be None")

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

        for item in ["name", "type", "quantity", "price", "add_insurance", "is_fragile"]:
            if item not in self.details["items"]:
                raise KeyError(f"{item} missing in items")

        # routes
        for _, value in self.details["routes"].items():
            if value is None or type(value) is not float:
                raise TypeError("Invalid routes data")

    def get_delivery_price(self):
        self.validate()
        print("[WeGoo order delivery validation passed]")

        data = {
            "is_fulfillment_delivery": self.is_fulfilment_delivery,
            "service": self.service,
            "details": self.details,
        }

        try:
            response = requests.post(
                url=self.create_delivery_price_url, json=data, headers=self.headers
            )
            if response.status_code == 201:
                result = response.json()
                print("result from wegoo", result)
            return True
        except Exception as e:
            print(f"[WeGoo Create Delivery Price Exception]: {str(e)}")
            return False

    def create_delivery(self):
        print("creating wegoo delivery...")
        self.validate()
