from django.contrib import admin
from src.apps.orders.models import Order, OrderItem, Location

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Location)

# Register your models here.
