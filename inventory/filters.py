import django_filters

from inventory.models import InventoryLog


class InventoryLogFilter(django_filters.FilterSet):
    received_date__isnull = django_filters.BooleanFilter(
        field_name="received_date", lookup_expr="isnull"
    )

    class Meta:
        model = InventoryLog
        fields = [
            "received_date__isnull",
        ]
