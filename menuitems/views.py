from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from menuitems.filters import MenuItemFilter
from menuitems.models import LimitedTimePromotion, MenuItem
from menuitems.serializers.limited_time_promotion import LimitedTimePromotionSerializer
from menuitems.serializers.menu_item import (
    MenuItemDetailSerializer,
    MenuItemSerializer,
    MenuItemSummarySerializer,
)


class MenuItemViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    http_method_names = ["post", "get"]
    model = MenuItem
    queryset = model.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MenuItemFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MenuItemDetailSerializer
        elif self.action == "list":
            return MenuItemSummarySerializer
        return MenuItemSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class LimitedTimePromotionViewSet(
    AutocompleteViewSetMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    http_method_names = ["post", "get", "put"]
    model = LimitedTimePromotion
    queryset = model.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    serializer_class = LimitedTimePromotionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_archived"]
