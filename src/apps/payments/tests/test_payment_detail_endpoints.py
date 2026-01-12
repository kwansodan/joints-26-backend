from decimal import Decimal
from django.urls import reverse
from src.apps.payments.tests.factory import create_payment
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.bikers.tests.factory import create_biker
from src.apps.vendors.tests.factory import create_menuitem, create_vendor
from src.apps.orders.tests.factory import create_location, create_order, create_orderitem

class TestPaymentDetailEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        customer_user = create_user(email="customer@gmail.com", phone="+11454785623")
        vendor_user = create_user(email="vendor@gmail.com", phone="+781454785623")
        vendor = create_vendor(user=vendor_user, name="Mimi's Kitchen")
        menuitem = create_menuitem(vendor=vendor, name="Barbecue Grill")
        orderitem = create_orderitem(menuitem=menuitem, quantity=11)
        location = create_location(displayName="Achimota", latitude=Decimal(4.5), longitude=Decimal(33.6))
        order = create_order(customer=customer_user, orderItem=orderitem, location=location)
        payment = create_payment(order=order, paymentMethod="bank", paymentReference="pref9uio")
        self.url = reverse("payments:payment-detail-view", kwargs={"pk": payment.pk})

        # targets
        self.target_customer_user = create_user(email="targetcustomer@gmail.com", phone="+454654804654")
        self.target_vendor_user = create_user(email="targetvendor@gmail.com", phone="+781454785623")
        self.target_vendor = create_vendor(user=self.target_vendor_user, name="Target Kitchen & Grill")
        self.target_menuitem = create_menuitem(vendor=self.target_vendor, name="Fufu Delight")
        self.target_orderitem = create_orderitem(menuitem=self.target_menuitem, quantity=3)
        self.target_location = create_location(displayName="Achimota", latitude=Decimal(88.5), longitude=Decimal(112.3))
        self.target_order = create_order(customer=self.target_customer_user, orderItem=self.target_orderitem, location=self.target_location)

    # anonymous
    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_update(self):
        user = create_user(email="userconfirm@gmail.com", userType="agent")
        paymentMethod = "momo"
        paymentReference = "prhhskdhii"
        response = self.client.put(self.url, {"order": self.target_order.pk, "paymentMethod": paymentMethod, "paymentReference": paymentReference, "confirmedBy": user.pk}, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_delete(self):
        response = self.client.delete(self.url)
        self.assertIn(response.status_code, [401, 403])

    # with permission
    def test_get_payment_detail_success(self):
        user = create_user(permissions=["payments.view_payment"])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_payment_detail_success(self):
        user = create_user(email="userconfirm@gmail.com", userType="agent", permissions=["payments.change_payment"])
        self.authenticate(user)
        paymentMethod = "momo"
        paymentReference = "prhhskdhii"
        response = self.client.put(self.url, {"order": self.target_order.pk, "paymentMethod": paymentMethod, "paymentReference": paymentReference, "confirmedBy": user.pk}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_payment_detail_success(self):
        user = create_user(permissions=["payments.delete_payment"])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)

    # without permission
    def test_get_payment_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_payment_without_permission_is_denied(self):
        user = create_user(email="userconfirm@gmail.com", userType="agent")
        self.authenticate(user)
        paymentMethod = "momo"
        paymentReference = "userpass123"
        response = self.client.put(self.url, {"order": self.target_customer_user.pk, "paymentMethod": paymentMethod, "paymentReference": paymentReference, "confirmedBy": user.pk}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_delete_payment_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)






