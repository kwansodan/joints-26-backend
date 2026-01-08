from rest_framework.permissions import BasePermission

ALLOWED_ROLES = {"admin", "biker"}

class BikerPermissions(BasePermission):
    perms_by_method = {
        "GET": "bikers.view_biker",
        "POST": "bikers.add_biker",
        "PUT": "bikers.change_biker",
        "PATCH": "bikers.change_biker",
        "DELETE": "bikers.delete_biker",
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

class BikerVehiclePermissions(BasePermission):
    perms_by_method = {
        "GET": "bikers.view_bikervehicle",
        "POST": "bikers.add_bikervehicle",
        "PUT": "bikers.change_bikervehicle",
        "PATCH": "bikers.change_bikervehicle",
        "DELETE": "bikers.delete_bikervehicle",
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

BikerPermissionList = [BikerPermissions, BikerVehiclePermissions]
