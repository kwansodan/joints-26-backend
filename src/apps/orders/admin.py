from django.contrib import admin
from src.apps.orders.models import Order, OrderItem, OrderLocation

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderLocation)

# Register your models here.
