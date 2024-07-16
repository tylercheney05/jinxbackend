from rest_framework.permissions import BasePermission, IsAdminUser

SAFE_METHODS = ["GET"]


class IsSystemAdminUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)


class IsSystemAdminUserOrIsStaffUserReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and request.user and request.user.is_staff
        ) or bool(request.user and request.user.is_admin)
