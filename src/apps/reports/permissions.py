from rest_framework.permissions import BasePermission

ALLOWED_ROLES = {"admin"}

class ReportModelPermission(BasePermission):
    perms_by_method = {
        "GET": "reports.view_report",
        "POST": "reports.add_report",
        "PUT": "reports.change_report",
        "PATCH": "reports.change_report",
        "DELETE": "reports.delete_report",
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

