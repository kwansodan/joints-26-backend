import requests
from django.conf import settings

API_KEY = settings.MNOTIFY_API_KEY 

class Mnotifiy:
    def __init__(self, recipients=[], message=None):
        self.sender = "Lingo"
        self.recipients = recipients 
        self.message = message
        self.url = f"https://api.mnotify.com/api/sms/quick?key={API_KEY}"
        self.headers =  {
            "Content-Type": "application/json"
        }

    def validate_info(self):
        if len(self.recipients) < 1:
            return False, "No recipients provided"

        for recipient in self.recipients:
            if len(recipient) < 10:
                return False, "Invalid recipient number"
    
        if self.message is None:
            return False, "No message provided"


    def send(self):
        try:
            self.validate_info()

            data = {
              "recipient": self.recipients, 
              "sender": self.sender,
              "message": self.message,
              "is_schedule": False,
              "schedule_date": ""
            }

            response = requests.post(url=self.url, json=data, headers=self.headers)
            result = response.json()
            print("result", result)

            if response.status_code == 200:
                return True, "sent"
        except Exception as e:
            print("exception from mnotify", str(e))
            return False, str(e)


if __name__ == "__main__":
    mnotify = Mnotifiy(["0545723325", "0503768479"], "testing mnotify api")
    mnotify.send()



