from secrets import token_urlsafe
from src.apps.users.models import User
from src.utils.dbOptions import USER_TYPES
from django.contrib.auth.models import Group
from src.apps.users.serializers import AuthSerializer

# users
def usersListService():
    status = False
    message = None
    data = None
    try:
        users = User.objects.filter(is_staff=False, is_superuser=False)
        serializer = AuthSerializer(instance=users, many=True)
        if serializer:
            status = True
            message = "success"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[UserService Err] Failed to get users list: {e}")
    return status, message, data
    
def createUserService(userData):
    status = False
    message = None
    data = None
    try:
        data = userData.copy()
        data["password"] = token_urlsafe(10) 
        serializer = AuthSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            status = True
            message = "User created successfully"
            data = serializer.data
        else:
            message = serializer.errors
    except Exception as e:
        print(f"[UserService Err] Failed to add user: {e}")
    return status, message, data

def getUserDetailService(pk):
    status = False
    message = "no user found"
    data = None
    try:
        userObj = User.objects.get(pk=pk)
        if userObj:
            serializer = AuthSerializer(instance=userObj)
            status = True
            message = "success"
            data = serializer.data
    except Exception as e:
        print(f"[UserService Err] Failed to get user detail: {e}")
    return status, message, data

def updateUserService(pk, requestData):
    status = False
    message = "user does not exists" 
    data = None
    try:
        user = User.objects.get(pk=pk)
        if user:
            serializer = AuthSerializer(instance=user, data=requestData, partial=True)
            if serializer.is_valid():
                serializer.save()
                status = True
                message = "success"
                data = serializer.data
            else:
                status = False
                message = serializer.errors
    except Exception as e:
        print(f"[UserService Err] Failed to update user: {e}")
    return status, message, data

def deleteUserService(userId):
    status = False
    message = "user doest not exists" 
    data = None
    try:
        user = User.objects.get(pk=userId)
        if user:
            user.delete()
            status = True
            message = "success"
    except Exception as e:
        print(f"[UserService Err] Failed to delete user: {e}")
    return status, message, data

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
