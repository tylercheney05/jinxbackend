from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from core.permissions import IsSystemAdminUser
from inventory.filters import InventoryItemFilter, InventoryLogFilter
from inventory.models import InventoryCategory, InventoryItem, InventoryLog
from inventory.serializers import (
    InventoryCategorySerializer,
    InventoryItemSerializer,
    InventoryItemSerializerReadOnly,
    InventoryLogSerializer,
)


class InventoryCategoryViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    http_method_names = ["post", "get"]
    queryset = InventoryCategory.objects.all()
    serializer_class = InventoryCategorySerializer
    permission_classes = [IsSystemAdminUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name"]
    ordering = ["name"]


class InventoryItemViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    http_method_names = ["post", "get", "patch"]
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsSystemAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = InventoryItemFilter
    ordering_fields = ["name"]
    ordering = ["category__name", "name"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return InventoryItemSerializerReadOnly
        return InventoryItemSerializer


class InventoryLogViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    http_method_names = ["post", "get", "patch"]
    queryset = InventoryLog.objects.all()
    serializer_class = InventoryLogSerializer
    permission_classes = [IsSystemAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = InventoryLogFilter
