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
        destination_metadata={},
        origin_metadata={},
        destination_routes={},
        origin_routes={},
        items=[],
    ):
        self.is_fulfilment_delivery = is_fulfillment_delivery
        self.service = service
        self.destination_metadata = destination_metadata
        self.origin_metadata = origin_metadata
        self.destination_routes = destination_routes
        self.origin_routes = origin_routes
        self.items = items
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
        self.create_delivery_price_url = (
            "https://api.wegoo.delivery/v1/deliveries/price"
        )

    def validate(self):
        assert self.destination_metadata is not None
        assert self.origin_metadata is not None
        assert self.destination_routes is not None
        assert self.origin_routes is not None
        assert self.items is not None

        # destination metadata
        assert (
            self.destination_metadata["destination_country"] is not None
        ), "destination country not provided"
        assert (
            self.destination_metadata["destination"] is not None
        ), "destination not provided"
        assert (
            self.destination_metadata["destination_city"] is not None
        ), "destination city not provided"
        assert (
            self.destination_metadata["destination_state"] is not None
        ), "destination state not provided"

        # origin metadata
        assert (
            self.origin_metadata["origin_country"] is not None
        ), "origin country not provided"
        assert self.origin_metadata["origin"] is not None, "origin not provided"
        assert (
            self.origin_metadata["origin_city"] is not None
        ), "origin city not provided"
        assert (
            self.origin_metadata["origin_state"] is not None
        ), "origin state not provided"

        # destination routes 
        assert isinstance(
            self.destination_routes["latitude"], float
        ), "destination route has no latitude"
        assert isinstance(
            self.destination_routes["longitude"], float
        ), "destination route has no longitude"

        # origin routes
        assert isinstance(
            self.origin_routes["latitude"], float
        ), "origin route has no latitude"
        assert isinstance(
            self.origin_routes["longitude"], float
        ), "origin route has no longitude"

        # items
        assert len(self.items) > 0, "No items in provided"
        for item in self.items:
            assert item["name"] is not None, "item has no name"
            assert item["type"] is not None, "item has no type"
            assert item["quantity"] is not None, "item has no quantity"
            assert item["price"] is not None, "item has no price"
            assert item["is_fragile"] is not None, "item has no prop for is_fragile"
            assert item["add_insurance"] is not None, "item has no prop for add_insurance"

    def create_delivery_price(self):
        self.validate()
        print("[WeGoo order delivery validation passed]")

        data = {
            "is_fulfillment_delivery": self.is_fulfilment_delivery,
            "service": self.service,
            "details": [
                {
                    **self.destination_metadata,
                    **self.origin_metadata,
                    "routes": {
                        "origin": self.origin_routes,
                        "destination": self.destination_routes,
                    },
                    "items": self.items,
                }
            ],
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

