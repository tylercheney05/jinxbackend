from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from inventory.models import InventoryCategory, InventoryItem, InventoryLog


class InventoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryCategory
        fields = [
            "id",
            "name",
        ]
        read_only_fields = ["id"]


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "name",
            "category",
            "sku",
            "unit_size",
            "uom",
            "reorder_point",
            "order_cost",
            "order_count",
        ]
        read_only_fields = ["id"]


class InventoryItemSerializerReadOnly(ReadOnlyModelSerializer):
    category = InventoryCategorySerializer()

    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "name",
            "category",
            "sku",
            "unit_size",
            "uom",
            "reorder_point",
            "order_cost",
            "order_count",
            "on_hand_qty",
            "in_transit_qty",
            "min_order_qty",
            "reorder_status",
        ]


class InventoryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLog
        fields = [
            "id",
            "inventory_item",
            "quantity",
            "purchase_date",
            "received_date",
            "note",
        ]
        read_only_fields = ["id"]
