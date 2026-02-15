from django.contrib import admin
from src.apps.payments.models import Payment, PaystackTransactionReference

admin.site.register(Payment)
admin.site.register(PaystackTransactionReference)

# Register your models here.
