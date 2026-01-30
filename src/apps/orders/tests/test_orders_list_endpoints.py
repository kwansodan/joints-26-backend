from decimal import Decimal
from django.urls import reverse
from src.apps.orders.tests.factory import create_location, create_orderitem
from src.apps.vendors.serializers import MenuItemSerializer
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.vendors.tests.factory import create_vendor, create_menuitem

class TestOrderListEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("orders:order-list-view")

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

    # def test_create_order_success(self):
    #     user = create_user(permissions=["orders.add_order"])
    #     self.authenticate(user)
    #     customer_user = create_user(email="customer@gmail.com", userType="customer")
    #     vendor_user = create_user(email="vendor@gmail.com", userType="vendor")
    #     vendor = create_vendor(user=vendor_user, name="Pizzman") 
    #     location = create_location(displayName="Israel", latitude=Decimal(8.8), longitude=Decimal(1.0))
    #
    #     menuitem1 = create_menuitem(vendor=vendor, name="Fried Chips")
    #     print("menu item id", menuitem1.id)
    #     # menuitem1 = MenuItemSerializer(instance=menuitem1).data
    #     # orderitem1 = create_orderitem(menuitem=menuitem1, quantity=4)
    #
    #     # menuitem2 = create_menuitem(vendor=vendor, name="Fried Chips")
    #     # orderitem2 = create_orderitem(menuitem=menuitem2, quantity=4)
    #
    #     payload =  {
    #             "customer": customer_user.pk,
    #             # "orderItem": orderitem1.pk,
    #             "location": location.pk,
    #             "orderItems": [menuitem1.id],
    #     }
    #     response = self.client.post(self.url, payload, format="json")
    #     self.assertEqual(response.status_code, 201)

