from django.core.management.base import BaseCommand
from src.services.users import updateAllUserGroups

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        updateAllUserGroups()

