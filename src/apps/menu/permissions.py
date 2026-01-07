from rest_framework.permissions import BasePermission

ALLOWED_ROLES = {"admin", "agent"}

class MenuModelPermission(BasePermission):
    perms_by_method = {
        "GET": "menu.view_menu",
        "POST": "menu.add_menu",
        "PUT": "menu.change_menu",
        "PATCH": "menu.change_menu",
        "DELETE": "menu.delete_menu",
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


