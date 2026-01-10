from decimal import Decimal
from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user

class TestLocationListEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("orders:location-list-view")

    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [401, 403])

    def test_user_with_invalid_role_is_denied(self):
        user = create_user(userType="customer")
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_user_without_view_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_create_location_success(self):
        user = create_user(permissions=["orders.add_location"])
        self.authenticate(user)
        payload =  {
            "displayName": "Tabora",
            "latitude": Decimal(1.5),
            "longitude": Decimal(5.5),
            "region": "Greater Accra",
            "district": "Ga West",
            "city": "Accra",
            "houseNumber": "GW-1234-5678",
            "road": "Chantan",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 201)
