from rest_framework.permissions import BasePermission

ALLOWED_ROLES = {"admin", "agent"}

class PaymentModelPermission(BasePermission):
    perms_by_method = {
        "GET": "payments.view_payment",
        "POST": "payments.add_payment",
        "PUT": "payments.change_payment",
        "PATCH": "payments.change_payment",
        "DELETE": "payments.delete_payment",
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

