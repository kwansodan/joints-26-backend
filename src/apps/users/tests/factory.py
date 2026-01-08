from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

User = get_user_model()

def create_user(
    *,
    email="admin@gmail.com",
    password="securepass@123",
    userType="admin",
    permissions=None
):
    user = User.objects.create_user(
        email=email,
        password=password,
        userType=userType
    )

    if permissions:
        for perm in permissions:
            user.user_permissions.add(
                Permission.objects.get(codename=perm.split(".")[1])
            )

    return user
