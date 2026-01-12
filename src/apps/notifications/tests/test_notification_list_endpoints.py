from decimal import Decimal
from django.urls import reverse
from src.apps.orders.tests.factory import create_location, create_order, create_orderitem
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.vendors.tests.factory import create_vendor, create_menuitem

class TestPaymentListEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("notifications:notification-list-view")

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

    def test_create_notification_success(self):
        user = create_user(permissions=["notifications.add_notification"])
        self.authenticate(user)
        sender = create_user(email="sender@gmail.com", userType="agent")
        receiver = create_user(email="vendor@gmail.com", userType="customer")
        notificationType = "sms"
        topic = "Payment Confirmed"
        message = f"Hello, {receiver.first_name}, your payment has been successfully received. Regards, Lingo"
        payload =  [
            {
                "sender": sender.pk,
                "receiver": receiver.pk,
                "notificationType": notificationType,
                "topic": topic,
                "message": message,
            },
        ]
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 201)

