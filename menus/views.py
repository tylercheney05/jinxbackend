from rest_framework import mixins, viewsets

from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from menus.models import Menu
from menus.serializers import MenuSerializer


class MenuViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    http_method_names = ["post", "get"]
    queryset = Menu.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    serializer_class = MenuSerializer
