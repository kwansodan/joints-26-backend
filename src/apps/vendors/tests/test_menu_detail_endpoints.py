from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.vendors.tests.factory import create_menuitem, create_vendor

class TestMenuDetailEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        user = create_user(email="vendor@gmail.com")
        vendor = create_vendor(user=user, name="KFC", location="North Legon", phone="+224153655256")
        menu = create_menuitem(vendor=vendor)
        self.url = reverse("vendors:menu-detail-view", kwargs={"pk": menu.pk})

    # anonymous
    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_update(self):
        new_user = create_user(email="newuser@gmail.com")
        new_vendor_name = "Papaye"
        new_location = "Lapaz"
        new_phone = "+233564154758"
        response = self.client.put(self.url, {"user": new_user.pk, "name": new_vendor_name, "location": new_location, "phone": new_phone}, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_delete(self):
        response = self.client.delete(self.url)
        self.assertIn(response.status_code, [401, 403])

    # with permission
    def test_get_menu_detail_success(self):
        user = create_user(permissions=["vendors.view_menuitem"])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_menu_detail_success(self):
        user = create_user(permissions=["vendors.change_menuitem"])
        self.authenticate(user)
        new_menu_name = "Banku & Tilapia"
        new_user = create_user(email="newvendoruser@gmail.com")
        new_vendor = create_vendor(user=new_user, name="Chef's In", location="Madina")
        response = self.client.put(self.url, {"vendor": new_vendor.pk, "name": new_menu_name, "description": "New menu description", "price": 55.50}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_menu_detail_success(self):
        user = create_user(permissions=["vendors.delete_menuitem"])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)

    # without permission
    def test_get_menu_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_menu_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        new_menu_name = "Banku & Tilapia"
        new_user = create_user(email="newvendoruser@gmail.com")
        new_vendor = create_vendor(user=new_user, name="Chef's In", location="Madina")
        response = self.client.put(self.url, {"vendor": new_vendor.pk, "name": new_menu_name, "description": "New menu description", "price": 125.50}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_delete_menu_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)






