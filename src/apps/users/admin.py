from django.contrib import admin

admin.site.site_header = "LINGO ADMIN"

from src.apps.users.models import Customer, User

admin.site.register(User)
admin.site.register(Customer)
