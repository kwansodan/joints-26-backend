from rest_framework.permissions import BasePermission

ALLOWED_ROLES = {"admin", "agent"}

class UserModelPermission(BasePermission):
    perms_by_method = {
        "GET": "users.view_user",
        "POST": "users.add_user",
        "PUT": "users.change_user",
        "PATCH": "users.change_user",
        "DELETE": "users.delete_user",
    }

    def has_permission(self, request, view):
        user = getattr(request, "user", None)

        if not user or not user.is_authenticated:
            return False

        if user.userType not in ALLOWED_ROLES:
            return False

        perm = self.perms_by_method.get(request.method)
        if not perm:
            return False

        return user.has_perm(perm)

class CustomerModelPermission(BasePermission):
    perms_by_method = {
        "GET": "users.view_customer",
        "POST": "users.add_customer",
        "PUT": "users.change_customer",
        "PATCH": "users.change_customer",
        "DELETE": "users.delete_customer",
    }

    def has_permission(self, request, view):
        user = getattr(request, "user", None)

        if not user or not user.is_authenticated:
            return False

        if user.userType not in ALLOWED_ROLES:
            return False

        perm = self.perms_by_method.get(request.method)
        if not perm:
            return False

        return user.has_perm(perm)
