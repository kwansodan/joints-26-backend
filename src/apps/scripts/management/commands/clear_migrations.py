from typing import Any
import os 
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand

BASE_DIR = settings.BASE_DIR

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        response = input("Are you sure you want to clear all migrations: (yes/no) ")
        
        if response == "yes":
            apps = ["users", "vendors", "bikers", "orders", "notifications", "payments", "external"]
            rm_dirs = ["migrations", "__pycache__"]

            try:
                for rdir in rm_dirs:
                    for app in apps:
                        dir = os.listdir(f"{BASE_DIR}/src/apps/{app}/{rdir}") 
                        for item in dir:
                            if item == "__init__.py" and rdir == "migrations":
                                continue 
                            try:
                                os.remove(f"{BASE_DIR}/src/apps/{app}/{rdir}/{item}")
                            except:
                                shutil.rmtree(f"{BASE_DIR}/src/apps/{app}/migrations/__pycache__")

                print("all migrations files deleted")
            except Exception as e:
                print(f"failed to delete migrations files: {str(e)}")
        else:
            print("cancelling")
