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


class InventoryLog(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateField()
    received_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, default="")
