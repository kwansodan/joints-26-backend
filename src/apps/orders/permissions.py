from rest_framework.permissions import BasePermission

ALLOWED_ROLES = {"admin", "agent"}

class LocationModelPermission(BasePermission):
    perms_by_method = {
        "GET": "orders.view_location",
        "POST": "orders.add_location",
        "PUT": "orders.change_location",
        "PATCH": "orders.change_location",
        "DELETE": "orders.delete_location",
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

class OrderItemModelPermission(BasePermission):
    perms_by_method = {
        "GET": "orders.view_orderitem",
        "POST": "orders.add_orderitem",
        "PUT": "orders.change_orderitem",
        "PATCH": "orders.change_orderitem",
        "DELETE": "orders.delete_orderitem",
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

class OrderModelPermission(BasePermission):
    perms_by_method = {
        "GET": "orders.view_order",
        "POST": "orders.add_order",
        "PUT": "orders.change_order",
        "PATCH": "orders.change_order",
        "DELETE": "orders.delete_order",
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


