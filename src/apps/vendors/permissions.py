from rest_framework.permissions import BasePermission

ALLOWED_ROLES = {"admin", "agent", "vendor"}

class VendorModelPermission(BasePermission):
    perms_by_method = {
        "GET": "vendors.view_vendor",
        "POST": "vendors.add_vendor",
        "PUT": "vendors.change_vendor",
        "PATCH": "vendors.change_vendor",
        "DELETE": "vendors.delete_vendor",
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

class MenuModelPermission(BasePermission):
    perms_by_method = {
        "GET": "vendors.view_menu",
        "POST": "vendors.add_menu",
        "PUT": "vendors.change_menu",
        "PATCH": "vendors.change_menu",
        "DELETE": "vendors.delete_menu",
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


