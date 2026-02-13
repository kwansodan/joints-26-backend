from pprint import pprint

import requests
from django.conf import settings

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
PAYSTACK_PUBLIC_KEY = settings.PAYSTACK_PUBLIC_KEY


class Paystack:
    def __init__(self):
        self.payment_page_url = "https://api.paystack.co/page"
        self.currency_sub_unit = 100
        self.currency = ("GHS",)
        self.accessibility_link_slug = "lingo-order-payments"
        self.payment_type = "payment"
        self.success_message = "Thank you for completing payment. Your order will be delivered soon."
        self.notification_email = "mohammedyiwere@gmail.com"
        self.headers = {
            "Authorization": f"Authorization: Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

    def validate(self):
        pass

    def _get_paystack_amount(self, amount: float):
        if not isinstance(amount, float):
            raise ValueError("amount must be float")
        return self.currency_sub_unit * amount

    def get_accessibility_link(self):
        if not self.accessibility_link_slug:
            raise ValueError("no accessibility link provided")
        return f"https://paystack.com/pay/{self.accessibility_link_slug }"

    def create_payment_page(self, amount):
        data = {
            "name": "Lingo",
            "description": "Make payment for your order",
            "amount": self._get_paystack_amount(amount),
            "currency": self.currency,
            "slug": self.accessibility_link_slug,
            "type": self.payment_type,
            "success_message": self.success_message,
            "notification_email": self.notification_email,

        }

        pprint(data, indent=2)
