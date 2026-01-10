from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user

class TestVendorListEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("vendors:vendor-list-view")

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

    def test_create_vendor_success(self):
        user = create_user(permissions=["vendors.add_vendor"])
        self.authenticate(user)
        user = create_user(email="vendor@gmail.com", userType="vendor")
        payload =  {
            "user": user.pk,
            "name": "Pizzaman",
            "location": "Haatso",
            "phone": "+23356415265"
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 201)
