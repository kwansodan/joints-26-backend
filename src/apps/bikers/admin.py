from django.contrib import admin

from src.apps.bikers.models import Biker, ParentDeliveryItem, ChildDeliveryItem, Vehicle


class ParentDeliveryItemModelAdmin(admin.ModelAdmin):
    list_display = (
        "orderId",
        "completed",
    )
    list_filter = ("orderId",)
    search_fields = ("orderId",)

class ChildDeliveryItemModelAdmin(admin.ModelAdmin):
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
admin.site.register(ParentDeliveryItem, ParentDeliveryItemModelAdmin)
admin.site.register(ChildDeliveryItem, ChildDeliveryItemModelAdmin)
