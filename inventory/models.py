from django.db import models


class InventoryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)


class InventoryItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, unique=True)
    unit_size = models.PositiveSmallIntegerField()
    uom = models.CharField(
        max_length=50,
        choices=[
            ("ct", "Count"),
            ("oz", "Ounce"),
            ("gal", "Gallon"),
            ("mL", "Milliliter"),
            ("L", "Liter"),
            ("QT", "Quart"),
        ],
    )
    reorder_point = models.PositiveIntegerField()
    order_cost = models.DecimalField(max_digits=10, decimal_places=2)
    order_count = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    @property
    def reorder_status(self):
        if self.reorder_point == 0:
            return "do_not_order"
        if self.on_hand_qty > self.reorder_point:
            return "ok"
        if self.on_hand_qty + self.in_transit_qty <= self.reorder_point:
            return "reorder"
        if self.in_transit_qty > 0:
            return "ordered"
        return None

    @property
    def in_transit_qty(self):
        return (
            self.inventorylog_set.filter(received_date__isnull=True).aggregate(
                total=models.Sum("quantity")
            )["total"]
            or 0
        )

    @property
    def on_hand_qty(self):
        return (
            self.inventorylog_set.filter(received_date__isnull=False).aggregate(
                total=models.Sum("quantity")
            )["total"]
            or 0
        )

    @property
    def min_order_qty(self):
        if self.reorder_point == 0:
            return 0
        return max(0, self.reorder_point - self.on_hand_qty - self.in_transit_qty)


class InventoryLog(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateField()
    received_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, default="")
