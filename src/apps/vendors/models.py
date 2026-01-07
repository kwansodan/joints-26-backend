from django.db import models
from src.utils.dbOptions import *
from src.utils.helpers import random_token

class Vendor(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    name = models.CharField(max_length=MAX_STR_LEN, unique=True, null=False, blank=True)
    location = models.CharField(max_length=MAX_STR_LEN, null=True, blank=True)
    phone = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    @property
    def menuList(self):
        from src.apps.menu.models import Menu
        from src.apps.menu.serializers import MenuSerializer
        menu = []
        try:
            obj = Menu.objects.filter(vendor=self)
            menu = MenuSerializer(instance=obj, many=True).data
        except Exception as e:
            print(f"error getting menulist for vendor: {e}")
        return menu

    class _Meta:
        verbose_name_plural = 'Vendors'
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.name} - {self.location}"
