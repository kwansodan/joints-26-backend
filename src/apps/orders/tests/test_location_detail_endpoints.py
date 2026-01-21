from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.bikers.tests.factory import create_biker
from src.apps.orders.tests.factory import create_location

class TestLocationDetailEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        location = create_location(displayName="Amasaman")
        self.url = reverse("orders:location-detail-view", kwargs={"pk": location.pk})

    # anonymous
    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_update(self):
        new_display_name = "Koforidua"
        new_lat = 3.3
        new_long = 6.3
        response = self.client.put(self.url, {"displayName": new_display_name, "latitude": new_lat, "longitude": new_long}, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_delete(self):
        response = self.client.delete(self.url)
        self.assertIn(response.status_code, [401, 403])

    # with permission
    def test_get_location_detail_success(self):
        user = create_user(permissions=["orders.view_location"])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_location_detail_success(self):
        user = create_user(permissions=["orders.change_location"])
        self.authenticate(user)
        new_display_name = "Koforidua"
        new_lat = 3.3
        new_long = 6.3
        response = self.client.put(self.url, {"displayName": new_display_name, "latitude": new_lat, "longitude": new_long}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_location_detail_success(self):
        user = create_user(permissions=["orders.delete_location"])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    # without permission
    def test_get_location_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_location_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        new_display_name = "Koforidua"
        new_lat = 3.3
        new_long = 6.3
        response = self.client.put(self.url, {"displayName": new_display_name, "latitude": new_lat, "longitude": new_long}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_delete_location_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)






