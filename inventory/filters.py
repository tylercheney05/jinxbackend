import django_filters

from inventory.models import InventoryItem, InventoryLog


class InventoryItemFilter(django_filters.FilterSet):
    class Meta:
        model = InventoryItem
        fields = ["is_active"]


class InventoryLogFilter(django_filters.FilterSet):
    received_date__isnull = django_filters.BooleanFilter(
        field_name="received_date", lookup_expr="isnull"
    )

    class Meta:
        model = InventoryLog
        fields = [
            "received_date__isnull",
        ]
