from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        bikerGroup, _ = Group.objects.get_or_create(name="biker")
        adminGroup, _ = Group.objects.get_or_create(name="admin")
        agentGroup, _ = Group.objects.get_or_create(name="agent")
        
        permissionActions = ["view", "add", "change", "delete"]

        adminPerms = {

            "users": [
                "user"
            ],

            "bikers": [
                "biker"
                "bikervehicle"
            ],

            "vendors": [
                "vendor"
            ],

            "menu": [
                "menu"
            ],

        }

        bikerPerms = {
            "bikers": [
                "biker"
                "bikervehicle"
            ],
        }

        agentPerms = {
            "bikers": [
                "biker"
                "bikervehicle"
            ],

            "vendors": [
                "vendor"
            ],

            "menu": [
                "menu"
            ],
        }

        # admin perms - [users, biker, bikerVehicle, menu, vendors]
        for app_label, models in adminPerms.items():
            for model in models:
                content_type = ContentType.objects.get(app_label=app_label, model=model)
                for action in permissionActions:
                    permission = Permission.objects.get(codename=f"{action}_{model}", content_type=content_type)
                    adminGroup.permissions.add(permission)
        
        # biker perms [biker & bikerVehicle]
        for app_label, models in bikerPerms.items():
            for model in models:
                content_type = ContentType.objects.get(app_label=app_label, model=model)
                for action in permissionActions:
                    permission = Permission.objects.get(codename=f"{action}_{model}", content_type=content_type)
                    bikerGroup.permissions.add(permission)
        
        # agent perms [biker, bikerVehicle, vendors, menu]
        for app_label, models in bikerPerms.items():
            for model in models:
                content_type = ContentType.objects.get(app_label=app_label, model=model)
                for action in permissionActions:
                    permission = Permission.objects.get(codename=f"{action}_{model}", content_type=content_type)
                    agentGroup.permissions.add(permission)
        


        print("done")
