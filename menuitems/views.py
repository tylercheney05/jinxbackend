from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from core.viewsets import AutocompleteViewSetMixin
from menuitems.filters import MenuItemFilter
from menuitems.models import LimitedTimePromotion, MenuItem
from menuitems.serializers import LimitedTimePromotionSerializer, MenuItemSerializer


class MenuItemViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    http_method_names = ["post", "get"]
    queryset = MenuItem.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MenuItemFilter


class LimitedTimePromotionViewSet(
    AutocompleteViewSetMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    http_method_names = ["post", "get"]
    queryset = LimitedTimePromotion.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    serializer_class = LimitedTimePromotionSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
