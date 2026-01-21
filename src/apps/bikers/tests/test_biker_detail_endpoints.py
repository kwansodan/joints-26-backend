from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.bikers.tests.factory import create_biker

class TestBikerDetailEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        target_biker_user = create_user(email="biker@gmail.com")
        target_biker = create_biker(user=target_biker_user)
        self.url = reverse("bikers:biker-detail-view", kwargs={"pk": target_biker.pk})

    # anonymous
    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_update(self):
        new_user = create_user(email="newuser@gmail.com")
        response = self.client.put(self.url, {"user": new_user.pk, "status": True, "totalTrips": 63}, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_delete(self):
        response = self.client.delete(self.url)
        self.assertIn(response.status_code, [401, 403])

    # with permission
    def test_get_biker_detail_success(self):
        user = create_user(permissions=["bikers.view_biker"])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_biker_detail_success(self):
        user = create_user(permissions=["bikers.change_biker"])
        self.authenticate(user)
        new_user = create_user(email="newuser@gmail.com")
        response = self.client.put(self.url, {"user": new_user.pk, "status": True, "totalTrips": 63}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_biker_detail_success(self):
        user = create_user(permissions=["bikers.delete_biker"])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    # without permission
    def test_get_biker_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_biker_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        new_user = create_user(email="newuser@gmail.com")
        response = self.client.put(self.url, {"user": new_user.pk, "status": True, "totalTrips": 63}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_delete_biker_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)






