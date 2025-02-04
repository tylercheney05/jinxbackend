from django.db import models


class CustomOrderFlavor(models.Model):
    """Flavors related to a CustomOrder"""

    flavor = models.ForeignKey(
        "flavors.Flavor", on_delete=models.CASCADE, related_name="custom_order_flavors"
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Custom Order {self.id} {self.flavor.name} {self.quantity}"


class CustomOrderFlavorCustomOrder(models.Model):
    """Model connecting the CustomOrderFlavor to the CustomOrder"""

    custom_order_flavor = models.OneToOneField(
        CustomOrderFlavor,
        on_delete=models.CASCADE,
        related_name="custom_order_flavor_custom_order",
    )
    custom_order = models.ForeignKey(
        "orders.CustomOrder",
        on_delete=models.CASCADE,
        related_name="custom_order_custom_order_flavors",
    )

    def __str__(self):
        return f"CustomOrderFlavorCustomOrder {self.id}"


class CustomOrderFlavorMenuItemCustomOrder(models.Model):
    """Model connecting the CustomOrderFlavor to the MenuItemCustomOrder"""

    custom_order_flavor = models.OneToOneField(
        CustomOrderFlavor,
        on_delete=models.CASCADE,
        related_name="custom_order_flavor_menu_item_custom_order",
    )
    menu_item_custom_order = models.ForeignKey(
        "orders.MenuItemCustomOrder",
        on_delete=models.CASCADE,
        related_name="menu_item_custom_order_custom_order_flavors",
    )

    def __str__(self):
        return f"CustomOrderFlavorMenuItemCustomOrder {self.id}"
