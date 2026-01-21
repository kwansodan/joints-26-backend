from decimal import Decimal
from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.bikers.tests.factory import create_biker
from src.apps.vendors.tests.factory import create_menuitem, create_vendor
from src.apps.orders.tests.factory import create_location, create_order, create_orderitem

class TestOrderDetailEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        customer_user = create_user(email="customer@gmail.com", phone="+11454785623")
        vendor_user = create_user(email="vendor@gmail.com", phone="+781454785623")
        vendor = create_vendor(user=vendor_user, name="Mimi's Kitchen")
        menuitem = create_menuitem(vendor=vendor, name="Barbecue Grill")
        orderitem = create_orderitem(menuitem=menuitem, quantity=11)
        location = create_location(displayName="Achimota", latitude=Decimal(4.5), longitude=Decimal(33.6))
        order = create_order(customer=customer_user, orderItem=orderitem, location=location)
        self.url = reverse("orders:order-detail-view", kwargs={"pk": order.pk})

        # targets
        self.target_customer_user = create_user(email="targetcustomer@gmail.com", phone="+454654804654")
        self.target_vendor_user = create_user(email="targetvendor@gmail.com", phone="+781454785623")
        self.target_vendor = create_vendor(user=self.target_vendor_user, name="Target Kitchen & Grill")
        self.target_menuitem = create_menuitem(vendor=self.target_vendor, name="Fufu Delight")
        self.target_orderitem = create_orderitem(menuitem=self.target_menuitem, quantity=3)
        self.target_location = create_location(displayName="Achimota", latitude=Decimal(88.5), longitude=Decimal(112.3))

    # anonymous
    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_update(self):
        response = self.client.put(self.url, {"customer": self.target_customer_user.pk, "orderItem": self.target_orderitem.pk, "location": self.target_location.pk}, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_delete(self):
        response = self.client.delete(self.url)
        self.assertIn(response.status_code, [401, 403])

    # with permission
    def test_get_order_detail_success(self):
        user = create_user(permissions=["orders.view_order"])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_order_detail_success(self):
        user = create_user(permissions=["orders.change_order"])
        self.authenticate(user)
        new_user = create_user(email="newuser@gmail.com")
        response = self.client.put(self.url, {"customer": self.target_customer_user.pk, "orderItem": self.target_orderitem.pk, "location": self.target_location.pk}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_order_detail_success(self):
        user = create_user(permissions=["orders.delete_order"])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    # without permission
    def test_get_order_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_order_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.put(self.url, {"customer": self.target_customer_user.pk, "orderItem": self.target_orderitem.pk, "location": self.target_location.pk}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_delete_order_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)






