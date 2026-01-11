from decimal import Decimal
from django.urls import reverse
from src.apps.orders.tests.factory import create_location, create_order, create_orderitem
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.vendors.tests.factory import create_vendor, create_menuitem

class TestPaymentListEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("payments:payment-list-view")

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

    def test_create_payment_success(self):
        user = create_user(permissions=["payments.add_payment"])
        self.authenticate(user)
        customer_user = create_user(email="customer@gmail.com", userType="customer")
        vendor_user = create_user(email="vendor@gmail.com", userType="vendor")
        vendor = create_vendor(user=vendor_user, name="Pizzman") 
        location = create_location(displayName="Israel", latitude=Decimal(8.8), longitude=Decimal(1.0))
        menuitem = create_menuitem(vendor=vendor, name="Fried Chips")
        orderitem = create_orderitem(menuitem=menuitem, quantity=4)
        order = create_order(customer=customer_user, orderItem=orderitem, location=location)

        payload =  [
            {
                "order": order.pk,
                "paymentMethod": "momo",
                "paymentReference": "hh8yo-(]",
                "confirmedBy": user.pk,
            },
        ]
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 201)

