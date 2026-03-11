from django.contrib import admin
from src.apps.vendors.models import Vendor, MenuItem, VendorLocation, VendorRedeemToken

admin.site.register(Vendor)
admin.site.register(MenuItem)
admin.site.register(VendorLocation)
admin.site.register(VendorRedeemToken)

