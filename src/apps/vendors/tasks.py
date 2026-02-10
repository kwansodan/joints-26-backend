from secrets import token_urlsafe

from celery import Task, shared_task
from django.conf import settings

from src.apps.external.models import GeneratedLink
from src.apps.vendors.models import Vendor, VendorLocation
from src.utils.dbOptions import TOKEN_LEN
from src.utils.sms_mnotify import Mnotifiy

FRONTEND_URL = settings.FRONTEND_URL


class BaseTaskWithRetry(Task):
    max_retries = 5
    default_retry_delay = 60


@shared_task(bind=True, base=BaseTaskWithRetry)
def send_vendor_location_capture_link(self, vendor_location_id: str):
    try:
        vendor_location = VendorLocation.objects.get(pk=vendor_location_id)
        vendor = Vendor.objects.get(id=vendor_location.vendor.id)
    except VendorLocation.DoesNotExist as e:
        raise self.retry(exc=e, countdown=60)

    if vendor_location.captured:
        return {
            "status": "Location already captured",
            "vendor_location_id": vendor_location.id,
        }

    url_token = token_urlsafe(TOKEN_LEN)
    link = f"{FRONTEND_URL}locationcapture/vendor/{url_token}/{vendor_location.id}"
    generated_link = GeneratedLink.objects.create(
        category="vendor", token=url_token, link=link
    )

    recipients = [vendor.phone]
    message = f"Hello {vendor.name}. Thanks for partnering with us. Please use the link below to share your location to start receiving orders. {generated_link.link}"

    print("mesage", message)

    # try:
    #     mnotify = Mnotifiy(recipients=recipients, message=message)
    #     _ = mnotify.send()
    # except Exception as exc:
    #     raise self.retry(exc=exc)

    return {
        "status": "vendor location capture link sent",
        "vendor_location_id": vendor_location_id,
    }
