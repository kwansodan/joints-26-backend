from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # regularGroup, _ = Group.objects.get_or_create(name="Regular")
        adminGroup, _ = Group.objects.get_or_create(name="admin")
        
        permissionActions = ["view", "add", "change", "delete"]

        adminPerms = {

            "users": [
                "user"
            ],

        }

        for app_label, models in adminPerms.items():
            for model in models:
                content_type = ContentType.objects.get(app_label=app_label, model=model)
                for action in permissionActions:
                    permission = Permission.objects.get(codename=f"{action}_{model}", content_type=content_type)
                    adminGroup.permissions.add(permission)
        
        print("done")
