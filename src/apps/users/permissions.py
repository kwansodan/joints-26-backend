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

    # def has_object_permission(self, request, view, obj):
    #     user = getattr(request, "user", None)
    #     if not user or not user.is_authenticated:
    #         return False
    #
    #     if user.userType == "admin":
    #         return True
    #     return False

"""
def check_object_permission(request, obj, permission_class):
    perm = permission_class()
    if not perm.has_object_permission(request, None, obj):
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied()
"""

"""
@api_view(["GET"])
@permission_classes([UserModelPermission])
def user_detail_view(request, user_id):
    user_obj = get_object_or_404(User, pk=user_id)
    check_object_permission(request, user_obj, UserModelPermission)
    return Response({"status": "ok", "data": user_obj.to_dict()})
"""

