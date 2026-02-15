from pprint import pprint

import requests
from django.conf import settings

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
PAYSTACK_PUBLIC_KEY = settings.PAYSTACK_PUBLIC_KEY

PAYMENT_REDIRECT_LINK = settings.PAYMENT_REDIRECT_LINK

class Paystack:
    def __init__(self, amount=None, email=None, reference=None, metadata={}):
        self.amount = amount
        self.email = email
        self.currency = "GHS"
        self.reference = reference
        self.metadata = metadata
        self.callback_url = PAYMENT_REDIRECT_LINK
        self.currency_sub_unit = 100
        self.base_transaction_url = "https://api.paystack.co/transaction"
        self.transaction_verification_url = "https://api.paystack.co/transaction/"
        self.channels = [
            "card",
            "bank",
            "apple_pay",
            "ussd",
            "qr",
            "mobile_money",
            "bank_transfer",
        ]
        self.headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

    def _get_paystack_amount(self):
        if not isinstance(self.amount, float):
            raise ValueError("amount must be float")
        amount = self.currency_sub_unit * self.amount
        return amount

    def get_transaction_url(self):
        try:

            data = {
                "email": self.email,
                "amount": self._get_paystack_amount(),
                "channels": self.channels,
                "currency": self.currency,
                "reference": self.reference,
                "metadata": self.metadata,
                "callback_url": self.callback_url
            }

            response = requests.post(
                f"{self.base_transaction_url}/initialize",
                json=data,
                headers=self.headers,
            )
            json_response = response.json()

            if response.status_code in [200, 201]:
                auth_url = json_response["data"]["authorization_url"]
                if auth_url is None or len(auth_url) < 1:
                    return False, None
                return True, auth_url
            else:
                return False, None
        except Exception as e:
            print("Paystack get transaction auth url exception", str(e))
            return False, None

    def verify_payment(self, reference):
        try:
            response = requests.get(f"{self.base_transaction_url}/verify/{reference}")
            json_response = response.json()
            print("response from verify payment", json_response)
            
            if response.status_code in [200, 201]:
                print("transaction valid")
                return True
            else:
                return False
        except Exception as e:
            print("Paystack payment verification exception", str(e))
            return False 
