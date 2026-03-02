from secrets import token_urlsafe

from django.contrib.auth.models import Group

from src.apps.users.models import User
from src.apps.users.serializers import AuthSerializer
from src.utils.dbOptions import USER_TYPES


# users
def usersListService():
    try:
        users = User.objects.filter(is_staff=False, is_superuser=False)
        serializer = AuthSerializer(instance=users, many=True)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[UserService Err] Failed to get users list: {e}")
        return False, "failed", None
    
def createUserService(userData):
    try:
        data = userData.copy()
        data["password"] = token_urlsafe(10) 
        serializer = AuthSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception as e:
        print(f"[UserService Err] Failed to add user: {e}")
        return False, "failed", None

def getUserDetailService(pk):
    try:
        userObj = User.objects.get(pk=pk)
        serializer = AuthSerializer(instance=userObj)
        return True, "success", serializer.data
    except Exception as e:
        print(f"[UserService Err] Failed to get user detail: {e}")
        return False, "failed", None

def updateUserService(pk, requestData):
    try:
        user = User.objects.get(pk=pk)
        serializer = AuthSerializer(instance=user, data=requestData, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return True, "success", serializer.data
    except Exception as e:
        print(f"[UserService Err] Failed to update user: {e}")
        return False, "failed", None

def deleteUserService(userId):
    try:
        user = User.objects.get(pk=userId)
        user.delete()
        return True, "success", None
    except Exception as e:
        print(f"[UserService Err] Failed to delete user: {e}")
        return False, "failed", None

# groups
def addUserToGroup(user):
    try:
        assert isinstance(user, User)
        agentGroup, _ = Group.objects.get_or_create(name="agent")
        bikerGroup, _ = Group.objects.get_or_create(name="biker")
        adminGroup, _ = Group.objects.get_or_create(name="admin")
        customerGroup, _ = Group.objects.get_or_create(name="customer")

        if user.userType == "agent":
            user.groups.add(agentGroup)

        elif user.userType == "biker":
            user.groups.add(bikerGroup)

        elif user.userType == "admin":
            user.groups.add(adminGroup)

        elif user.userType == "customer":
            user.groups.add(customerGroup)

    except Exception as e:
        print(f"err: failed to add user to group: {e}")

def updateAllUserGroups():
    try:
        agentGroup, _ = Group.objects.get_or_create(name="agent")
        bikerGroup, _ = Group.objects.get_or_create(name="biker")
        adminGroup, _ = Group.objects.get_or_create(name="admin")
        customerGroup, _ = Group.objects.get_or_create(name="customer")

        users = User.objects.all().only("id", "userType")
        for user in users:
            if user.userType == "agent":
                user.groups.add(agentGroup)

            elif user.userType == "biker":
                user.groups.add(bikerGroup)

            elif user.userType == "admin":
                user.groups.add(adminGroup)

            elif user.userType == "customer":
                user.groups.add(customerGroup)

    except Exception as e:
        print(f"err: failed to update user groups: {e}")
