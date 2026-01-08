from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user

class TestUserDetailEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        target_user = create_user(email="target@gmail.com")
        self.url = reverse("users:user-detail-view", kwargs={"pk": target_user.pk})

    # anonymous
    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_update(self):
        response = self.client.put(self.url, {"email": "updateduser@gmail.com"}, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_delete(self):
        response = self.client.delete(self.url)
        self.assertIn(response.status_code, [401, 403])

    # with permission
    def test_get_user_detail_success(self):
        user = create_user(permissions=["users.view_user"])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_user_detail_success(self):
        user = create_user(permissions=["users.change_user"])
        self.authenticate(user)
        response = self.client.put(self.url, {"email": "updateduser@gmail.com"}, json="format")
        self.assertEqual(response.status_code, 200)

    def test_delete_user_detail_success(self):
        user = create_user(permissions=["users.delete_user"])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)

    # without permission
    def test_get_user_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_user_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.put(self.url, {"email": "updatedemail@gmail.com"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_delete_user_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)






