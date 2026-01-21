from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.bikers.tests.factory import create_biker, create_vehicle

class TestVehicleDetailEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        user = create_user(email="targetbikeruser@gmail.com", userType="biker")
        biker = create_biker(user=user)
        target_vehicle = create_vehicle(biker=biker, licensePlate="GR-555-22")
        self.url = reverse("bikers:vehicle-detail-view", kwargs={"pk": target_vehicle.pk})

    # anonymous
    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_update(self):
        new_user = create_user(email="newuser@gmail.com")
        new_biker = create_biker(user=new_user)
        response = self.client.put(self.url, {"biker": new_biker.pk, "licensePlate": "XX-885-66", "registered": True, "vehicleType": "car"}, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_delete(self):
        response = self.client.delete(self.url)
        self.assertIn(response.status_code, [401, 403])

    # with permission
    def test_get_vehicle_detail_success(self):
        user = create_user(permissions=["bikers.view_vehicle"])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_vehicle_detail_success(self):
        user = create_user(permissions=["bikers.change_vehicle"])
        self.authenticate(user)
        new_user = create_user(email="newuser@gmail.com")
        new_biker = create_biker(user=new_user)
        response = self.client.put(self.url, {"biker": new_biker.pk, "licensePlate": "XX-885-66", "registered": True, "vehicleType": "car"}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_vehicle_detail_success(self):
        user = create_user(permissions=["bikers.delete_vehicle"])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    # without permission
    def test_get_vehicle_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_vehicle_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        new_user = create_user(email="newuser@gmail.com")
        new_biker = create_biker(user=new_user)
        response = self.client.put(self.url, {"biker": new_biker.pk, "licensePlate": "XX-885-66", "registered": True, "vehicleType": "car"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_delete_vehicle_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)






