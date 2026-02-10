from django.contrib import admin
from src.apps.vendors.models import Vendor, MenuItem, VendorLocation

admin.site.register(Vendor)
admin.site.register(MenuItem)
admin.site.register(VendorLocation)

