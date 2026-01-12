from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.vendors.tests.factory import create_vendor

class TestMenuListEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("vendors:menu-list-view")

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

    def test_create_menu_success(self):
        user = create_user(permissions=["vendors.add_menuitem"])
        self.authenticate(user)
        user = create_user(email="biker@gmail.com", userType="biker")
        vendor = create_vendor(user=user, name="Vendor1", location="Vendor location 1", phone="+233564585963")
        payload =  {
            "vendor": vendor.pk,
            "name": "Assorted Jollof Rice",
            "description": "Tasty and affordable assorted jollof rice",
            "price": 150.00
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 201)
