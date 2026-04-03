from rest_framework import filters, mixins, viewsets

from core.permissions import IsSystemAdminUser
from inventory.models import InventoryCategory, InventoryItem, InventoryLog
from inventory.serializers import InventoryCategorySerializer, InventoryItemSerializer, InventoryLogSerializer


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
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    http_method_names = ["post", "get"]
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsSystemAdminUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name"]
    ordering = ["category__name", "name"]


class InventoryLogViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    http_method_names = ["post", "get"]
    queryset = InventoryLog.objects.all()
    serializer_class = InventoryLogSerializer
    permission_classes = [IsSystemAdminUser]
