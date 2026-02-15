from django.contrib import admin

from src.apps.users.models import Customer, User

admin.site.register(User)
admin.site.register(Customer)
