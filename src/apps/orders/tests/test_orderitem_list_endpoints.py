from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.bikers.tests.factory import create_biker

class TestVehicleListEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("bikers:vehicle-list-view")

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

    def test_create_vehicle_success(self):
        user = create_user(permissions=["bikers.add_vehicle"])
        self.authenticate(user)
        biker_user = create_user(email="biker@gmail.com", userType="biker")
        biker = create_biker(user=biker_user)
        payload =  {
            "biker": biker.pk,
            "vehicleType": "motorbike",
            "licensePlate": "GW-123-45"
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 201)
