from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from menuitems.models import MenuItem
from menuitems.serializers import MenuItemSerializer


class MenuItemViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    http_method_names = ["post", "get"]
    queryset = MenuItem.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["soda"]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
