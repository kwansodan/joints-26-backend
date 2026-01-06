from django.db.models.signals import post_save
from django.dispatch import receiver
from src.apps.users.models import User
from src.services.users import addUserToGroup

@receiver(post_save, sender=User)
def createUserGroups(sender, instance, created, **kwargs):
    if created:
        addUserToGroup(instance)
