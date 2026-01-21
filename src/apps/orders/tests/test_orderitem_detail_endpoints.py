from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.orders.tests.factory import create_orderitem
from src.apps.bikers.tests.factory import create_biker, create_vehicle
from src.apps.vendors.tests.factory import create_menuitem, create_vendor

class TestOrderItemDetailEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        user = create_user(email="vendor@gmail.com", userType="vendor")
        vendor = create_vendor(user=user, name="Papaye")
        menuitem = create_menuitem(vendor=vendor, name="Banku & Tilapia")
        orderitem = create_orderitem(menuitem=menuitem, quantity=5)
        self.url = reverse("orders:orderitem-detail-view", kwargs={"pk": orderitem.pk})

    # anonymous
    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_update(self):
        new_user = create_user(email="newuser@gmail.com", userType="vendor")
        new_vendor = create_vendor(user=new_user, name="Test vendor 2")
        new_menuitem = create_menuitem(vendor=new_vendor, name="Pizza")
        new_quantity = 15
        response = self.client.put(self.url, {"menuitem": new_menuitem.pk, "quantiy": new_quantity}, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_delete(self):
        response = self.client.delete(self.url)
        self.assertIn(response.status_code, [401, 403])

    # with permission
    def test_get_orderitem_detail_success(self):
        user = create_user(permissions=["orders.view_orderitem"])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_orderitem_detail_success(self):
        user = create_user(permissions=["orders.change_orderitem"])
        self.authenticate(user)
        new_user = create_user(email="newuser@gmail.com", userType="vendor")
        new_vendor = create_vendor(user=new_user, name="Test vendor 2")
        new_menuitem = create_menuitem(vendor=new_vendor, name="Pizza")
        new_quantity = 15
        response = self.client.put(self.url, {"menuitem": new_menuitem.pk, "quantiy": new_quantity}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_orderitem_detail_success(self):
        user = create_user(permissions=["orders.delete_orderitem"])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    # without permission
    def test_get_orderitem_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_orderitem_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        new_user = create_user(email="newuser@gmail.com", userType="vendor")
        new_vendor = create_vendor(user=new_user, name="Test vendor 2")
        new_menuitem = create_menuitem(vendor=new_vendor, name="Pizza")
        new_quantity = 15
        response = self.client.put(self.url, {"menuitem": new_menuitem.pk, "quantiy": new_quantity}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_delete_orderitem_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)






