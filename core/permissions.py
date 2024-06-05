from rest_framework.permissions import IsAdminUser

class IsSystemAdminUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)