from rest_framework.permissions import BasePermission

ALLOWED_ROLES = {"admin", "agent"}

class NotificationModelPermission(BasePermission):
    perms_by_method = {
        "GET": "notifications.view_notification",
        "POST": "notifications.add_notification",
        "PUT": "notifications.change_notification",
        "PATCH": "notifications.change_notification",
        "DELETE": "notifications.delete_notification",
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

