from django.contrib import admin

from src.apps.bikers.models import Biker, Delivery, Vehicle


class DeliveryModelAdmin(admin.ModelAdmin):
    list_display = (
        "orderId",
        "deliveryTokenId",
        "completed",
        "vendorNotified",
        "dispatchServiceTrackingNumber",
        "dispatchServiceDeliveryType",
    )
    list_filter = ("deliveryTokenId",)
    search_fields = ("deliveryTokenId",)


admin.site.register(Biker)
admin.site.register(Vehicle)
admin.site.register(Delivery, DeliveryModelAdmin)
