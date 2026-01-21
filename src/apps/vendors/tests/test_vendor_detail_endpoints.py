from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.vendors.tests.factory import create_vendor

class TestVendorDetailEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        user = create_user(email="biker@gmail.com")
        vendor = create_vendor(user=user, name="KFC", location="North Legon", phone="+224153655256")
        self.url = reverse("vendors:vendor-detail-view", kwargs={"pk": vendor.pk})

    # anonymous
    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_update(self):
        new_user = create_user(email="newuser@gmail.com")
        new_vendor_name = "Grace's Kitchen"
        new_location = "Tema"
        response = self.client.put(self.url, {"user": new_user.pk, "name": new_vendor_name, "location": new_location, "phone": "+14252631155"}, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_delete(self):
        response = self.client.delete(self.url)
        self.assertIn(response.status_code, [401, 403])

    # with permission
    def test_get_vendor_detail_success(self):
        user = create_user(permissions=["vendors.view_vendor"])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_vendor_detail_success(self):
        user = create_user(permissions=["vendors.change_vendor"])
        self.authenticate(user)
        new_user = create_user(email="newuser@gmail.com")
        new_vendor_name = "Grace's Kitchen"
        new_location = "Tema"
        response = self.client.put(self.url, {"user": new_user.pk, "name": new_vendor_name, "location": new_location, "phone": "+14252631155"}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_vendor_detail_success(self):
        user = create_user(permissions=["vendors.delete_vendor"])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    # without permission
    def test_get_vendor_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_vendor_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        new_user = create_user(email="newuser@gmail.com")
        new_vendor_name = "Grace's Kitchen"
        new_location = "Tema"
        response = self.client.put(self.url, {"user": new_user.pk, "name": new_vendor_name, "location": new_location, "phone": "+14252631155"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_delete_vendor_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)






