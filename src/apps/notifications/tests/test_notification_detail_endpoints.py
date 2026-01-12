from django.urls import reverse
from src.utils.helpers import BaseAPITestCase
from src.apps.users.tests.factory import create_user
from src.apps.notifications.tests.factory import create_nofitication

class TestNotificationDetailEndpoints(BaseAPITestCase):
    def setUp(self):
        super().setUp()

        sender = create_user(email="sender@gmail.com", userType="agent")
        receiver = create_user(email="vendor@gmail.com", userType="customer")
        notificationType = "sms"
        topic = "Payment Confirmed"
        message = f"Hello, {receiver.first_name}, your payment has been successfully received. Regards, Lingo"
        notification = create_nofitication(
            sender=sender,
            receiver=receiver,
            topic=topic,
            message=message,
            notificationType=notificationType
        )
        self.url = reverse("notifications:notification-detail-view", kwargs={"pk": notification.pk})

        # targets
        self.target_sender = create_user(email="targetsender@gmail.com", phone="+454654804654")
        self.target_receiver = create_user(email="targetreceiver@gmail.com", phone="+781454785623")
        self.target_topic = "New target topic"
        self.target_message = "New target message"
        self.target_notificationType = "email"

    # anonymous
    def test_anonymous_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_update(self):
        response = self.client.put(self.url, {"sender": self.target_sender.pk, "receiver": self.target_receiver.pk, "topic": self.target_topic, "message": self.target_message, "notificationType": self.target_notificationType}, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_anonymous_user_cannot_delete(self):
        response = self.client.delete(self.url)
        self.assertIn(response.status_code, [401, 403])

    # with permission
    def test_get_notification_detail_success(self):
        user = create_user(permissions=["notifications.view_notification"])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_notification_detail_success(self):
        user = create_user(email="userconfirm@gmail.com", userType="agent", permissions=["notifications.change_notification"])
        self.authenticate(user)
        response = self.client.put(self.url, {"sender": self.target_sender.pk, "receiver": self.target_receiver.pk, "topic": self.target_topic, "message": self.target_message, "notificationType": self.target_notificationType}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_notification_detail_success(self):
        user = create_user(permissions=["notifications.delete_notification"])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)

    # without permission
    def test_get_notification_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_update_notification_without_permission_is_denied(self):
        user = create_user(email="notification@gmail.com", userType="agent")
        self.authenticate(user)
        response = self.client.put(self.url, {"sender": self.target_sender.pk, "receiver": self.target_receiver.pk, "topic": self.target_topic, "message": self.target_message, "notificationType": self.target_notificationType}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_delete_notification_without_permission_is_denied(self):
        user = create_user(permissions=[])
        self.authenticate(user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)






