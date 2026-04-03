from decimal import Decimal

from django.db.models import DecimalField, ExpressionWrapper, F, FloatField, Q, Sum
from django.db.models.functions import Cast
from django.db.models.functions import Coalesce

from inventory.models import InventoryItem


def get_inventory_item_values():
    """
    Return an InventoryItem queryset annotated with `item_value`:
        item_value = (order_cost / order_count) * SUM(inventorylog.quantity)
    Items with no logs get item_value = 0. Lazy — one DB query when evaluated.
    """
    return InventoryItem.objects.annotate(
        item_value=ExpressionWrapper(
            ExpressionWrapper(
                F("order_cost") / Cast("order_count", output_field=FloatField()),
                output_field=DecimalField(max_digits=20, decimal_places=2),
            )
            * Coalesce(
                Sum(
                    "inventorylog__quantity",
                    filter=Q(inventorylog__received_date__isnull=False),
                ),
                0,
            ),
            output_field=DecimalField(max_digits=20, decimal_places=2),
        )
    )


def get_total_inventory_value():
    """
    Return the sum of (order_cost / order_count * total_quantity) across all InventoryItems
    as a Decimal. Returns Decimal('0') when table is empty. One DB query.
    """
    result = get_inventory_item_values().aggregate(
        total=Sum(
            "item_value", output_field=DecimalField(max_digits=20, decimal_places=2)
        )
    )
    return result["total"] or Decimal("0")
