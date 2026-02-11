from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        bikerGroup, _ = Group.objects.get_or_create(name="biker")
        adminGroup, _ = Group.objects.get_or_create(name="admin")
        agentGroup, _ = Group.objects.get_or_create(name="agent")

        permissionActions = ["view", "add", "change", "delete"]

        userAppPerms = {"users": ["user"]}
        bikerAppPerms = {"bikers": ["biker", "vehicle"]}
        vendorAppPerms = {
            "vendors": [
                "vendor",
                "menuitem",
                "vendorlocation",
            ]
        }
        orderAppPerms = {"orders": ["location", "orderitem", "order"]}

        bikerPerms = [bikerAppPerms]
        adminPerms = [userAppPerms, bikerAppPerms, vendorAppPerms, orderAppPerms]
        agentPerms = [userAppPerms, bikerAppPerms, bikerAppPerms]

        # admin perms
        for appPerm in adminPerms:
            for app_label, models in appPerm.items():
                for model in models:
                    content_type = ContentType.objects.get(
                        app_label=app_label, model=model
                    )
                    for action in permissionActions:
                        permission = Permission.objects.get(
                            codename=f"{action}_{model}", content_type=content_type
                        )
                        adminGroup.permissions.add(permission)

        # biker perms
        for appPerm in bikerPerms:
            for app_label, models in appPerm.items():
                for model in models:
                    content_type = ContentType.objects.get(
                        app_label=app_label, model=model
                    )
                    for action in permissionActions:
                        permission = Permission.objects.get(
                            codename=f"{action}_{model}", content_type=content_type
                        )
                        bikerGroup.permissions.add(permission)

        # agent perms
        for appPerm in agentPerms:
            for app_label, models in appPerm.items():
                for model in models:
                    content_type = ContentType.objects.get(
                        app_label=app_label, model=model
                    )
                    for action in permissionActions:
                        permission = Permission.objects.get(
                            codename=f"{action}_{model}", content_type=content_type
                        )
                        agentGroup.permissions.add(permission)

        print("done")
