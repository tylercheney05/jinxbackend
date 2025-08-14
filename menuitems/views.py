from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from core.mixins import AutocompleteViewSetMixin
from core.permissions import IsSystemAdminUserOrIsStaffUserReadOnly
from menuitems.filters import MenuItemFilter
from menuitems.models import LimitedTimePromotion, MenuItem
from menuitems.serializers.limited_time_promotion import LimitedTimePromotionSerializer
from menuitems.serializers.menu_item import (
    MenuItemSerializer,
    MenuItemSerializerReadOnly,
)


class MenuItemViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    http_method_names = ["post", "get"]
    queryset = MenuItem.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MenuItemFilter
    ordering_fields = ["name"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MenuItemSerializerReadOnly
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
    queryset = LimitedTimePromotion.objects.all()
    permission_classes = [IsSystemAdminUserOrIsStaffUserReadOnly]
    serializer_class = LimitedTimePromotionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_archived"]
